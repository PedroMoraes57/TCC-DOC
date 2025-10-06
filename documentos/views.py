from django.views.generic import CreateView
from django.urls import reverse_lazy
from documentos.models import Documento
from documentos.forms import DocumentoForm
from documentos.services import extrair_texto_de_filefield  # OCR
from IA.services import classificar_documento  # IA/Gemini


class DigitalizarDocumento(CreateView):
    model = Documento
    form_class = DocumentoForm
    template_name = 'documentos/DigitalizarDocumentos.html'
    success_url = reverse_lazy('perfil')

    def form_valid(self, form):
        # Pega o arquivo do formulário
        arquivo = form.cleaned_data.get('arquivo')
        
        # 1️⃣ Extrai texto do PDF ou imagem
        texto_extraido = extrair_texto_de_filefield(arquivo)

        if not texto_extraido:
            # Não salva nada se OCR falhar
            form.add_error(None, "Não foi possível extrair texto do arquivo. Upload cancelado.")
            return self.form_invalid(form)

        # 2️⃣ Chama a IA/Gemini para corrigir e classificar
        try:
            dados = classificar_documento(texto_extraido)  # já retorna dict

            texto_corrigido = dados.get('corrected_text', texto_extraido)
            assunto = dados.get('assunto', '')
            setor = dados.get('setor', '')
            tipo = dados.get('tipo', '')
            prazo = dados.get('prazo', '')

        except Exception as e:
            print(f"[ERRO Gemini] {e}")
            # fallback seguro
            texto_corrigido = texto_extraido
            assunto = ''
            setor = ''
            tipo = ''
            prazo = ''

        # 3️⃣ Salva o documento no banco
        documento = form.save(commit=False)
        documento.conteudo_extraido = texto_corrigido
        documento.assunto = assunto
        documento.setor = setor
        documento.tipo = tipo
        documento.prazo = prazo  
        documento.save()

        return super().form_valid(form)
