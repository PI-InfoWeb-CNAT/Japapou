from django.db import models  # type: ignore


class Prato(models.Model):
    name = models.CharField(null=False, max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    descricao = models.TextField(null=False)
    foto = models.ImageField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    altered_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"nome: {self.name}"