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
