from django.db import models
from django.db.models import fields
from rest_framework import serializers
from clinica.models import *

class EspecialidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidade
        fields = '__all__'
        #fields = ['id', 'nome', 'rg', 'cpf', 'data_nascimento']


class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = '__all__'


class AgendaSerializer(serializers.ModelSerializer):
    # medico = serializers.ReadOnlyField(source='nome')
    # data = serializers.SerializerMethodField()
    # horario = serializers.SerializerMethodField()
    class Meta:
        model = Agenda
        fields = '__all__'
    
    def get_periodo(self, obj):
        return obj.get_periodo_display()


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'