from django.db import models  # type: ignore


class Order(models.Model):
    date = models.DateField()
    estimate = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    altered_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ["date"]

    def __str__(self):
        return f"{self.date.strftime('%d/%m/%Y')} - R$ {self.total}"

class Order_Pickup(Order):
    pickup_date = models.DateField()

    class Meta:
        verbose_name = "Pedido Retirada"
        verbose_name_plural = "Pedidos Retirados"

    def __str__(self):
        return f"Retirado em {self.pickup_date.strftime('%d/%m/%Y %H:%M')}"
    

class Order_Delivery(Order):
    delivery_fee  = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    dispatch_date = models.DateTimeField()
    delivery_date = models.DateTimeField()

    class Meta:
        verbose_name = "Pedido Delivery"
        verbose_name_plural = "Pedidos Delivery"

    def __str__(self):
        return f"Saiu do restaurante às {self.dispatch_date}, foi entregue às {self.delivery_date}"