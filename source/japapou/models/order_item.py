# japapou/models/order_item.py
from django.db import models  # type: ignore
from japapou.models.plate import Plate
from .order import Order

class OrderItem(models.Model):
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE, 
        related_name="items" 
    )
    

    
    prato = models.ForeignKey(Plate, on_delete=models.CASCADE, default=1, related_name='order_items_prato')
    amount = models.IntegerField()
    comment = models.TextField(null=True, blank=True) # Permitir nulo/branco
    created_at = models.DateTimeField(auto_now_add=True)
    altered_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Item de Pedido"
        verbose_name_plural = "Itens de Pedidos"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.amount} : {self.comment}"