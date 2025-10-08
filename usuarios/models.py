from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField

class Usuario(AbstractUser):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    pais = CountryField(blank_label="Selecione um país")
    telefone = models.CharField(max_length=25)
    foto_perfil = models.ImageField(upload_to="usuarios/perfis/", blank=True, null=True)

    def __str__(self):
        return self.username


class Feedback(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, f"{i}⭐") for i in range(1, 6)])
    comment = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.rating}⭐"
