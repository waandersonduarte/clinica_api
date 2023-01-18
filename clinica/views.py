from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from clinica.serializers import *
from clinica.models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import BaseAuthentication, BasicAuthentication, SessionAuthentication
from django.contrib.auth.forms import UserCreationForm

class EspecialidadeViewSet(viewsets.ModelViewSet):
    """Listando especialidades"""
    queryset = Especialidade.objects.all()
    serializer_class = EspecialidadeSerializer
    permission_classes = [IsAuthenticated]
    #authentication_classes = [BasicAuthentication]
    
# class MovieExampleView(APIView):
#     def get(self, request, format=None):
#         content = {
#             'user': str(request.user),
#             'auth': str(request.auth),
#         }
#         return Response(content)

class MedicoViewSet(viewsets.ModelViewSet):
    """Listando especialidades"""
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    permission_classes = [IsAuthenticated]


class AgendaViewSet(viewsets.ModelViewSet):
    """Listando especialidades"""
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer
    permission_classes = [IsAuthenticated]


    

class ClienteViewSet(viewsets.ModelViewSet):
    """Listando especialidades"""
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ConsultaViewSet(viewsets.ModelViewSet):
    """Listando especialidades"""
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer
    permission_classes = [IsAuthenticated]
    # def autenticar_cliente(request):
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     user = authenticate(request, username=username, password=password)
    authentication_classes = [BasicAuthentication]
    
    

    
