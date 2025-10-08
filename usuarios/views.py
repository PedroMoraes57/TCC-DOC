from .models import Usuario, Feedback
from django.views.generic import CreateView
from .forms import FeedbackForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, CadastroForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
# Create your views here.

def pagina_login(request):
    return render(request, 'usuarios/login.html')

class perfil(CreateView):
    model = Usuario
    template_name = 'usuarios/TemplatePerfil.html'
    fields = "__all__"

@login_required
def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.usuario = request.user  # associa o usuário logado
            feedback.save()
            return redirect('feedback')
    else:
        form = FeedbackForm()

    feedbacks = Feedback.objects.order_by('-created_at')
    return render(request, 'index.html', {'form': form, 'feedbacks': feedbacks})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
        else:
            print(form.errors)  # pra debug, vê o erro no terminal
    else:
        form = LoginForm()

    return render(request, "usuarios/login.html", {"form": form})


def cadastro_view(request):
    if request.method == "POST":
        form = CadastroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CadastroForm()

    return render(request, "usuarios/cadastro.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("home")

@login_required
def perfil_editar(request):
    user = request.user
    if request.method == "POST":
        user.nome = request.POST.get("nome")
        user.email = request.POST.get("email")
        user.telefone = request.POST.get("telefone")

        if "foto_perfil" in request.FILES:
            user.foto_perfil = request.FILES["foto_perfil"]

        user.save()
        messages.success(request, "Perfil atualizado com sucesso!")
        return redirect("perfil")

    return render(request, "perfil.html", {"user": user})