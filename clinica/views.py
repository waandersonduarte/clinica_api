from rest_framework import viewsets
from clinica.serializers import *
from clinica.models import *

class EspecialidadeViewSet(viewsets.ModelViewSet):
    """Listando especialidades"""
    queryset = Especialidade.objects.all()
    serializer_class = EspecialidadeSerializer

class MedicoViewSet(viewsets.ModelViewSet):
    """Listando especialidades"""
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer

class AgendaViewSet(viewsets.ModelViewSet):
    """Listando especialidades"""
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    """Listando especialidades"""
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer