from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView
from .models import Documento
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DeleteView
from .forms import DocumentoForm
from .services import extrair_texto_de_filefield
from IA.services import classificar_documento # ajuste se o import for outro
from django.contrib import messages


class DigitalizarDocumento(LoginRequiredMixin, CreateView):
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
            form.add_error(None, "Não foi possível extrair texto do arquivo. Upload cancelado.")
            return self.form_invalid(form)

        # 2️⃣ Chama a IA/Gemini para corrigir e classificar
        try:
            dados = classificar_documento(texto_extraido)
            texto_corrigido = dados.get('corrected_text', texto_extraido)
            assunto = dados.get('assunto', '')
            setor = dados.get('setor', '')
            tipo = dados.get('tipo', '')
            prazo = dados.get('prazo', '')
        except Exception as e:
            print(f"[ERRO Gemini] {e}")
            texto_corrigido = texto_extraido
            assunto = setor = tipo = prazo = ''

        # 3️⃣ Salva o documento no banco, agora com o usuário logado
        documento = form.save(commit=False)
        documento.usuario = self.request.user  # ← ISSO AQUI É O VÍNCULO FALTANTE
        documento.conteudo_extraido = texto_corrigido
        documento.assunto = assunto
        documento.setor = setor
        documento.tipo = tipo
        documento.prazo = prazo
        documento.save()

        return super().form_valid(form)


class ListarDocumentos(LoginRequiredMixin, ListView):
    model = Documento
    template_name = 'usuarios/TemplatePerfil.html'
    context_object_name = 'documentos'
    
    def get_queryset(self):
        # só mostra documentos do usuário logado
        return Documento.objects.filter(usuario=self.request.user).order_by('-id')

class DeletarDocumento(LoginRequiredMixin, DeleteView):
    model = Documento
    success_url = reverse_lazy('perfil')  # redireciona pra lista de documentos
    template_name = 'usuarios/TemplatePerfil.html'  # opcional

    def get_queryset(self):
        # segurança: só deixa o usuário deletar os próprios documentos
        return Documento.objects.filter(usuario=self.request.user)