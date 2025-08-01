from django.db import models  # type: ignore


class OrderItem(models.Model):
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
