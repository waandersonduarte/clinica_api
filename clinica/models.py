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

