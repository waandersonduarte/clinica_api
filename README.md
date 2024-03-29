# API - Django Rest Framework
O Django Rest Framework auxilia na usabilidade do sistema facilitando a manipulação das informações contidas no Banco de Dados. O intuito do projeto é o desenvolvimento de uma API com simulação de uma clinica. Sendo assim, o sistema tem as seguintes funcionalidades: cadastro de especialidades, médicos, agendas, clientes e a possibilidade dos clientes/pacientes marcar consultas de acordo a disponibilidade da agenda dos médicos. O sistema contém as seguintes restrições: Não deve ser possível criar mais de uma agenda para um médico em um mesmo dia e não deve ser possível criar uma agenda para um médico em um dia passado. Além disso, contém sistema de autenticação e serialização dos dados.
## Criando o diretório do projeto
```
mkdir clinica_api
cd clinica_api
```

## Criando o ambiente virtual
```
virtualenv venv
. venv/bin/activate  
```

## Instalando as ferramentas necessárias para nossa aplicação
```
pip install django
pip install djangorestframework
pip install markdown       
pip install django-filter
```

## Criando o projeto e a aplicação
```
django-admin startproject core .  
django-admin startapp clinica
```

## Configurando o settings.py
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'clinica',
]
```

## Criando os modelos para nossa clinica
No arquivo ``clinica/models.py`` definimos todos os objetos chamados Modelos, este é um lugar em que vamos definir os relacionamentos entre as classes que estaram presentes na nossa clinica definidos no nosso diagrama e classes.

Vamos abrir ``clinica/models.py`` no editor de código, apagar tudo dele e escrever o seguinte código:
```python
from django.db import models
from django.contrib.auth.models import User

class Especialidade(models.Model):
    nome = models.CharField(max_length=50, blank=False, verbose_name='Especialidade:')

    def __str__(self):
        return self.nome


class Medico(models.Model):
    nome = models.CharField(max_length=50, blank=False, verbose_name='Nome:')
    crm = models.CharField(max_length=20, blank=False, verbose_name='CRM:')
    email = models.EmailField(max_length=30, verbose_name='E-mail:')
    telefone = models.CharField(max_length=14, verbose_name='Telefone:')
    especialidade_nome = models.ForeignKey(Especialidade, on_delete=models.CASCADE, verbose_name='Especialidade:')

    def __str__(self):
        return self.nome


class Agenda(models.Model):
    nome_medico = models.ForeignKey(Medico, on_delete=models.CASCADE, blank=False, verbose_name='Nome do Médico:')
    data = models.DateField(blank=False, verbose_name='Data:')
    horario = models.TimeField(blank=False, verbose_name='Horário:')

    @property
    def data_horario(self):
        return f'{self.data.strftime("%d/%m/%Y")} | {self.horario.strftime("%H:%M") or ""} | ({self.nome_medico})'.strip()

    def __str__(self):
        return str(self.data_horario)


class Cliente(User):
    SEXO = (
        ('M', 'Masculino'),
        ('F', 'Feminino'))
    nome = models.CharField(max_length=50, blank=False, verbose_name='Nome:')
    cpf = models.CharField(max_length=11, blank=False, verbose_name='CPF:')
    sexo = models.CharField(max_length=1, choices=SEXO, null=False, default='M', verbose_name='Gênero:')
    telefone = models.CharField(max_length=14, verbose_name='Telefone:')

    def __str__(self):
        return self.nome
        

class Consulta(models.Model):
    nome_medico = models.ForeignKey(Medico, on_delete=models.CASCADE, verbose_name='Nome do Médico:')
    data_agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE, verbose_name='Data e Horário:')

    def __str__(self):
        return self.nome_medico
```
Preparar e migrar nossos modelos para a base de dados:
```
python manage.py makemigrations
python manage.py migrate
```
## Admin
```
python manage.py createsuperuser
```
Vamos abrir o arquivo ``clinica/admin.py``, apagar tudo e acrescentar o seguinte código:
```python
from django.contrib import admin
from django.contrib.auth import admin as admin_add
from clinica.models import *

class Especialidades(admin.ModelAdmin):
    list_display = ('id', 'nome')
    list_display_links = ('id', 'nome')
    search_fields = ('nome',)
    list_filter = ('nome',)
    
    list_per_page = 15
    ordering = ('nome',)

admin.site.register(Especialidade, Especialidades)


class Medicos(admin.ModelAdmin):
    list_display = ('id', 'nome', 'crm', 'email','telefone', 'especialidade_nome')
    list_display_links = ('id', 'nome')
    search_fields = ('nome',)
    list_filter = ('nome',)
    
    list_per_page = 15
    ordering = ('nome',)

admin.site.register(Medico, Medicos)

class Agendas(admin.ModelAdmin):
    list_display = ('id', 'nome_medico', 'data', 'horario')
    list_display_links = ('id', 'nome_medico')
    search_fields = ('nome_medico',)
    list_filter = ('nome_medico',)
   
    list_per_page = 15
    ordering = ('nome_medico',)

admin.site.register(Agenda, Agendas)

class Clientes(admin.ModelAdmin):
    list_display = ('id', 'nome', 'cpf', 'email', 'sexo', 'telefone')
    list_display_links = ('id', 'nome')
    search_fields = ('nome',)
    list_filter = ('nome',)
  
    list_per_page = 15
    ordering = ('nome',)

admin.site.register(Cliente, Clientes)

class Consultas(admin.ModelAdmin):
    list_display = ('id', 'nome_medico', 'data_agenda')
    list_display_links = ('id', 'nome_medico')
    search_fields = ('nome_medico',)
    list_filter = ('nome_medico',)
  
    list_per_page = 15
    ordering = ('nome_medico',)

admin.site.register(Consulta, Consultas)
```

## Serializers
Iremos criar um arquivo ``clinica/serializers.py``:

```python
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


class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = '__all__'


class AgendaSerializer(serializers.ModelSerializer):
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
```

## Views
Vamos abrir ``clinica/views.py`` no editor de código, apagar tudo dele e escrever o seguinte código:
```python
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
```

## Routers
Vamos editar ``core/urls.py`` no editor de código:
```python
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
    path('admin/', admin.site.urls),
]

```
## Testando a API
Vamos startar o servidor web
```
python manage.py runserver
```
```
http://127.0.0.1:8000/
```
