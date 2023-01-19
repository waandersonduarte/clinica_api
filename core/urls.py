from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from clinica.views import *

router = routers.DefaultRouter()
router.register('especialidades', EspecialidadeViewSet)
router.register('medicos', MedicoViewSet)
router.register('agendas', AgendaViewSet)
router.register('clientes', ClienteViewSet)
router.register('marcar_consulta', ConsultaViewSet) 

urlpatterns = [
    path('', include(router.urls)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]
