from django.db import models  # type: ignore


class Plate(models.Model):
    name = models.CharField(null=False, max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    description = models.TextField(null=False)
    photo = models.ImageField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    altered_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Prato"
        verbose_name_plural = "Pratos"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} (R$ {self.price}): {self.description}"
