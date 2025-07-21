from django.db import models  # type: ignore
from .prato import Prato
from .cardapio import Cardapio

class Menu(models.Model):
    data_ini = models.DateField()
    data_fim = models.DateField()
    pratos = models.ForeignKey(Prato, on_delete=models.CASCADE, null=True)
    cardapio = models.ForeignKey(Cardapio, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Descricao: {self.cardapio.descricao} - Prato: {self.pratos.name}"