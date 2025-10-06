import io
import os
import tempfile
from PIL import Image, UnidentifiedImageError
import fitz  # PyMuPDF
import pytesseract
import cv2
import numpy as np
from docx import Document  # Novo

def preprocess_image(file_bytes):
    """Pré-processa imagem para OCR"""
    nparr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.medianBlur(thresh, 3)
    pil_img = Image.fromarray(blur)
    return pil_img

def extrair_texto_de_filefield(filefield):
    """
    Recebe um FileField e retorna texto extraído.
    Funciona para PDFs, imagens e DOCX.
    Retorna None se não conseguir extrair nada.
    """
    content = filefield.read()
    filename = filefield.name.lower()

    # --- DOCX ---
    if filename.endswith('.docx'):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                tmp.write(content)
                tmp_path = tmp.name
            doc = Document(tmp_path)
            texto = "\n".join([p.text for p in doc.paragraphs]).strip()
            return texto if texto else None
        except Exception:
            return None
        finally:
            try:
                os.remove(tmp_path)
            except OSError:
                pass

    # --- PDF ---
    if filename.endswith('.pdf') or content[:4] == b'%PDF':
        texto = ""
        try:
            with fitz.open(stream=content, filetype="pdf") as pdf:
                for pagina in pdf:
                    texto += pagina.get_text("text")
            texto = texto.strip()
            return texto if texto else None
        except Exception:
            return None

    # --- Imagem ---
    try:
        img_pre = preprocess_image(content)
        texto = pytesseract.image_to_string(img_pre, lang='por', config="--oem 1 --psm 3").strip()
        return texto if texto else None
    except UnidentifiedImageError:
        # fallback: salvar temporariamente e tentar abrir como imagem
        suffix = os.path.splitext(filename)[1] or '.bin'
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        try:
            try:
                img = Image.open(tmp_path)
                if img.mode != "RGB":
                    img = img.convert("RGB")
                # aplica pré-processamento
                img_bytes = tmp.read() if hasattr(tmp, "read") else open(tmp_path, "rb").read()
                img_pre = preprocess_image(img_bytes)
                texto = pytesseract.image_to_string(img_pre, lang='por', config="--oem 1 --psm 3").strip()
                return texto if texto else None
            except Exception:
                return None
        finally:
            try:
                os.remove(tmp_path)
            except OSError:
                pass

    return None
