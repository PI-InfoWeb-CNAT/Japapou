from django.db import models  # type: ignore


class User(models.Model):
    name = models.CharField(null=False, max_length=100)
    cpf = models.CharField(null=False, max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    altered_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
