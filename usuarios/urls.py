from django.urls import path
from . import views
from documentos.views import ListarDocumentos
from documentos.views import DeletarDocumento
from django.contrib.auth.views import LogoutView
from .views import login_view, cadastro_view, logout_view

urlpatterns = [
    path('perfil/', ListarDocumentos.as_view(), name='perfil'),
    path('feedback/', views.feedback_view, name='feedback'),
    path("login/", views.login_view, name="login"),
    path("cadastro/", views.cadastro_view, name="cadastro"),
    path('deletar/<int:pk>/', DeletarDocumento.as_view(), name='deletar_documento'),
    path('logout/', logout_view, name='logout'),
    path("perfil/editar/", views.perfil_editar, name="perfil_editar"),
]