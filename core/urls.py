from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from clinica.views import *

router = routers.DefaultRouter()
router.register('especialidades', EspecialidadeViewSet, basename='especialidades')
router.register('medicos', MedicoViewSet, basename='medicos')
router.register('agendas', AgendaViewSet, basename='agendas')
router.register('clientes', ClienteViewSet, basename='clientes')
router.register('marcar_consulta', ConsultaViewSet, basename='marcar_consulta') 

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
