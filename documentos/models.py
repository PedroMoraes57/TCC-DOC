from django.db import models
from usuarios.models import Usuario

class Documento(models.Model):
    arquivo = models.FileField(upload_to='documentos/', null=False, blank=False)
    nome = models.CharField(max_length=100, null=False, blank=False)
    tipo = models.CharField(max_length=20, null=True, blank=True) 
    setor = models.CharField(max_length=25, null=True, blank=True)
    assunto = models.CharField(max_length=200)
    conteudo_extraido = models.TextField(blank=True)
    data_modificacao = models.DateTimeField(auto_now=True)
    data_publicacao = models.DateField(null=True, blank=True, auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)

    # Campos extra extraídos via OCR/IA
    prazo = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome