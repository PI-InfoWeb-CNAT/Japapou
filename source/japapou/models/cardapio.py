from django.db import models  # type: ignore

class Cardapio(models.Model):
    descricao = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    altered_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"nome: {self.descricao}"