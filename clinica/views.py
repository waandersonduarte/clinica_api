from django.shortcuts import render, redirect
from rest_framework import viewsets
from clinica.serializers import *
from clinica.models import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import BaseAuthentication, BasicAuthentication

class EspecialidadeViewSet(viewsets.ModelViewSet):
    queryset = Especialidade.objects.all()
    serializer_class = EspecialidadeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]


class MedicoViewSet(viewsets.ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]


class AgendaViewSet(viewsets.ModelViewSet):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]



class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]
    
    

    
