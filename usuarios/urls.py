from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.pagina_login, name='login'),
    path('perfil/', views.perfil.as_view(), name='perfil'),
    path('feedback/', views.feedback_view, name='feedback'),
]