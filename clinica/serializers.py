from django.db import models
from django.db.models import fields
from rest_framework import serializers
from clinica.models import *
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

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

    def validate(self, data):
        data_atual = date.today()
    
        if data['data'] < data_atual:
            raise serializers.ValidationError({'data': 'Não é possível selecionar uma data que já passou!'})

        nome_medico = data['nome_medico']
        agenda_medico = Agenda.objects.filter(nome_medico__id = nome_medico.id)
        
        for agenda in agenda_medico:
            if data['data'] == agenda.data:
                raise serializers.ValidationError({'nome_medico': 'Não é possível fazer agendamento no mesmo dia para um único médico!'})               
        return data
        

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente 
        fields = ('nome', 'cpf','sexo', 'telefone', 'username', 'email', 'password')


class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        fields = '__all__'

        def validate(self, data):
        
    
            nome_medico = data['nome_medico']
            agenda_medico = Consulta.objects.filter(nome_medico__id = nome_medico.id)
            
            for agenda in agenda_medico:
                if data['nome_medico'] != agenda.nome_medico:
                    raise serializers.ValidationError({'nome_medico': 'Não é possível fazer agendamento com um médico diferente do selecionado!'})               
            return data