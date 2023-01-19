# Criando o diretório do projeto
```
mkdir clinica_api
cd clinica_api
```

# Criando o ambiente virtual
```
virtualenv venv
. venv/bin/activate  
```

# Instalando as ferramentas necessárias para nossa aplicação
```
pip install django
pip install djangorestframework
pip install markdown       
pip install django-filter
```

# Criando o projeto e a aplicação
```
django-admin startproject core .  
django-admin startapp clinica
```

# Configurando o settings.py
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', #novo
    'clientes', #novo
]
```

# Criando os modelos para nossa clinica
No arquivo ``clinica/models.py`` definimos todos os objetos chamados Modelos, este é um lugar em que vamos definir os relacionamentos entre as classes que estaram presentes na nossa clinica definidos no nosso diagrama e classes.

Vamos abrir clinica/models.py no editor de código, apagar tudo dele e escrever o seguinte código:
```python
from django.db import models

class Especialidade(models.Model):
    nome = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.nome


class Medico(models.Model):
    nome = models.CharField(max_length=50, blank=False)
    crm = models.CharField(max_length=20, blank=False)
    email = models.EmailField(max_length=30)
    telefone = models.CharField(max_length=14)
    especialidade_nome = models.ForeignKey(Especialidade, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Agenda(models.Model):
    nome_medico = models.ForeignKey(Medico, on_delete=models.CASCADE, blank=False)
    data = models.DateField(blank=False)
    horario = models.TimeField(blank=False)

    def __str__(self):
        return self.nome_medico


class Cliente(models.Model):
    SEXO = (
        ('M', 'Masculino'),
        ('F', 'Feminino'))
    nome = models.CharField(max_length=50, blank=False)
    cpf = models.CharField(max_length=11, blank=False)
    email = models.EmailField(max_length=30)
    sexo = models.CharField(max_length=1, choices=SEXO, null=False, default='M')
    telefone = models.CharField(max_length=14)

    def __str__(self):
        return self.nome
```
Preparar e migrar nossos modelos para a base de dados:
```
python manage.py makemigrations
python manage.py migrate
```
# Admin
```
python manage.py createsuperuser
```
Vamos abrir o arquivo ``clinica/admin.py``, apagar tudo e acrescentar o seguinte código:
```python
from django.contrib import admin
from clinica.models import *

class Especialidades(admin.ModelAdmin):
    list_display = ('id', 'nome')
    list_display_links = ('id', 'nome')
    search_fields = ('nome',)
    list_filter = ('nome',)
    list_editable = ('nome',)
    list_per_page = 15
    ordering = ('nome',)

admin.site.register(Especialidade, Especialidades)


class Medicos(admin.ModelAdmin):
    list_display = ('id', 'nome', 'crm', 'email','telefone', 'especialidade_nome')
    list_display_links = ('id', 'nome')
    search_fields = ('nome',)
    list_filter = ('nome',)
    list_editable = ('nome',)
    list_per_page = 15
    ordering = ('nome',)

admin.site.register(Medico, Medicos)

class Agendas(admin.ModelAdmin):
    list_display = ('id', 'nome_medico', 'data', 'horario')
    list_display_links = ('id', 'nome_medico')
    search_fields = ('nome_medico',)
    list_filter = ('nome_medico',)
    list_editable = ('nome_medico',)
    list_per_page = 15
    ordering = ('nome_medico',)

admin.site.register(Agenda, Agendas)

class Clientes(admin.ModelAdmin):
    list_display = ('id', 'nome', 'cpf', 'email', 'sexo', 'telefone')
    list_display_links = ('id', 'nome')
    search_fields = ('nome',)
    list_filter = ('nome',)
    list_editable = ('nome',)
    list_per_page = 15
    ordering = ('nome',)

admin.site.register(Cliente, Clientes)
```

# Serializers
Iremos criar um arquivo ``clinica/serializers.py``:

```python
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
    medico = serializers.ReadOnlyField(source='nome')
    data = serializers.SerializerMethodField()
    horario = serializers.SerializerMethodField()
    class Meta:
        model = Agenda
        fields = ['medico', 'data', 'horario']
    
    def get_periodo(self, obj):
        return obj.get_periodo_display()


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
```

# Views
Vamos abrir ``clinica/views.py`` no editor de código, apagar tudo dele e escrever o seguinte código:
```python
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
```

# Routers
Vamos editar core/urls.py no editor de código:
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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
```
# Testando a API
Vamos startar o servidor web
```
python manage.py runserver
```
```
http://127.0.0.1:8000/
```
