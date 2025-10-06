from django.shortcuts import render
from .models import Usuario, Feedback
from django.views.generic import CreateView
from .forms import FeedbackForm
# Create your views here.

def pagina_login(request):
    return render(request, 'usuarios/login.html')

class perfil(CreateView):
    model = Usuario
    template_name = 'usuarios/TemplatePerfil.html'
    fields = "__all__"

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('feedback')
    else:
        form = FeedbackForm()

    feedbacks = Feedback.objects.order_by('-created_at')
    return render(request, 'index.html', {'form': form, 'feedbacks': feedbacks})