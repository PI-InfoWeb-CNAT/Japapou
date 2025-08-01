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
