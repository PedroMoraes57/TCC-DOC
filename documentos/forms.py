from django import forms
from .models import Documento

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['nome', 'arquivo']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder':'Insira o nome do seu documento...'}),
            'arquivo': forms.ClearableFileInput(attrs={'placeholder':'Selecione ou arraste seu arquivo aqui.\nFormatos disponíveis: PDF, PNG, JPG, JPEG, Exel, DOC, DOCX', 'class':'arquivo-control'})
        }

