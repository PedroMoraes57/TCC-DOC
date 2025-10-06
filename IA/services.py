import google.generativeai as genai
import json

genai.configure(api_key="AIzaSyAgx50CP6LeC7pf9DQ4mewDQTKuhOVApPE")

def classificar_documento(texto: str) -> dict:
    if not isinstance(texto, str):
        texto = str(texto)

    prompt = f"""
Analise e classifique o texto fornecido.
Corrija erros gramaticais ou de digitação.

Extraia **apenas o prazo principal de entrega ou validade do documento**, ignorando prazos secundários (como aviso prévio, prorrogação, recurso, multa, etc.).

Texto:
---
"{texto}"
---

Retorne APENAS um JSON válido com as chaves:
{{
  "assunto": "",
  "setor": "",
  "tipo": "",
  "prazo": "",
  "corrected_text": ""
}}

Regras:
1. Se houver múltiplas datas, retorne SOMENTE a que indica o prazo de entrega, vigência ou validade.
2. Se não houver prazos de entrega/validade, retorne "Não identificado".
3. Não adicione texto fora do JSON.
4. Traduza qualquer texto contido no documento para português do Brasil.
"""

    dados_padrao = {
        "assunto": "Não foi possível classificar",
        "setor": "Não foi possível classificar",
        "tipo": "Não foi possível classificar",
        "corrected_text": texto,
        "prazo": "Não identificado"
    }

    try:
        model = genai.GenerativeModel("models/gemini-2.0-flash")
        resposta = model.generate_content(prompt)
        resposta_texto = resposta.text.strip().replace("```json", "").replace("```", "").strip()
        dados = json.loads(resposta_texto)

        for key in dados_padrao:
            if key not in dados or not dados[key]:
                dados[key] = dados_padrao[key]

    except Exception as e:
        print(">> Erro:", e)
        return dados_padrao

    return dados
