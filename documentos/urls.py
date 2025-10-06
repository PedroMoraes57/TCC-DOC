from django.urls import path, include 
from .views import DigitalizarDocumento

urlpatterns = [
    path('Digitalizar/', DigitalizarDocumento.as_view(), name="Digitalizar_Documentos")
]
