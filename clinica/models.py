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
    #horario_agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome_medico

