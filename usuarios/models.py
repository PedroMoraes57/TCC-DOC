from django.db import models
from django_countries.fields import CountryField
from django.conf import settings

## Esse modelo de usuário será corrigido, portanto, desconsidere o atual
class Usuario(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(null=False, blank=False, unique=True)
    pais = CountryField(blank_label=("Selecione um país"))
    telefone = models.CharField(max_length=25, null=False, blank=False)
    foto_perfil = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.nome
    
class Feedback(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.rating}⭐"