from django.db import models  # type: ignore
from .prato import Prato
from .cardapio import Cardapio

class Menu(models.Model):
    data_ini = models.DateField()
    data_fim = models.DateField()
    pratos = models.ManyToManyField(Prato, null=True, blank=True)
    cardapio = models.ForeignKey(Cardapio, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"

    def __str__(self):
        # Pega todos os nomes dos pratos relacionados e os junta com ', '
        nomes_dos_pratos = ", ".join([prato.name for prato in self.pratos.all()]) 
        # Verifica se o cardapio não é nulo antes de tentar acessar 'descricao'
        descricao_cardapio = self.cardapio.descricao if self.cardapio else "Sem Cardápio Associado"
        return f"Cardápio: {descricao_cardapio} - Período({self.data_ini} a {self.data_fim}) - Pratos: {nomes_dos_pratos}"