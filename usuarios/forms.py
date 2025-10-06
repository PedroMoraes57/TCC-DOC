from .models import Usuario, Feedback
from django import forms

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone'}),
        }
        
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['usuario', 'rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'placeholder': 'Escreva seu feedback...',
                'rows': 3
            }),
            'rating': forms.HiddenInput(),  # escondemos o campo e tratamos via JS
        }