from django.db import models  # type: ignore
from japapou.models.plate import Plate

class OrderItem(models.Model):
    order = models.ForeignKey('japapou.Order', on_delete=models.CASCADE, related_name='items')
    prato = models.ForeignKey(Plate, on_delete=models.CASCADE, default=1, related_name='items')
    amount = models.IntegerField()
    comment = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    altered_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Item de Pedido"
        verbose_name_plural = "Itens de Pedidos"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.amount} : {self.comment}"
