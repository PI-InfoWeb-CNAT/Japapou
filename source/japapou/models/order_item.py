# japapou/models/order_item.py
from django.db import models  # type: ignore
from japapou.models.plate import Plate
from .order import Order

class OrderItem(models.Model):
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE, 
        related_name="itens" 
    )
    
    '''
        mudar depois para guardar o preço do prato no momento da compra
        caso o preço do prato mude depois da compra
    '''
    
    preco_prato = models.DecimalField(max_digits=8, decimal_places=2, default=0.00) # Preço do prato no momento da compra
    prato = models.ForeignKey(Plate, on_delete=models.CASCADE, default=1, related_name='order_items_prato')
    amount = models.IntegerField(default=1)
    comment = models.TextField(null=True, blank=True) # Permitir nulo/branco
    created_at = models.DateTimeField(auto_now_add=True)
    altered_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Item de Pedido"
        verbose_name_plural = "Itens de Pedidos"
        ordering = ["created_at"]


    def get_item_total(self):
        return self.preco_prato * self.amount
    
    def __str__(self):
        prato_nome = getattr(self.prato, 'name', 'Prato Desconhecido') 
        return f"{self.amount}x {prato_nome} (Pedido: {self.order.id})"