from django.contrib import admin
from usuarios.models import Usuario
from documentos.models import Documento

admin.site.register(Usuario)
admin.site.register(Documento)