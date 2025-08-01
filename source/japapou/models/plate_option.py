from django.db import models  # type: ignore


class PlateOption(models.Model):
    description = models.TextField(null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    class Meta:
        verbose_name = "Opção de Prato"
        verbose_name_plural = "Opções de Pratos"
        ordering = ["description"]

    def __str__(self):
        return f"{self.description} (R$ {self.price})"
