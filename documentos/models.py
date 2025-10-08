from django.db import models
from usuarios.models import Usuario

class Documento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    arquivo = models.FileField(upload_to='documentos/')
    tipo = models.CharField(max_length=20)
    setor = models.CharField(max_length=25)
    assunto = models.CharField(max_length=200)
    conteudo_extraido = models.TextField(blank=True)
    prazo = models.CharField(max_length=100, blank=True, null=True)
    data_modificacao = models.DateTimeField(auto_now=True)
    data_publicacao = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.nome} ({self.usuario})" if self.usuario else self.nome
