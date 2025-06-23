from japapou.models import *

class Usuario(models.Model):
    nome = models.CharField(null=False, max_length=100)
    cpf = models.CharField(null=False, max_length=15)
    criado_em = models.DateTimeField(auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.nome)