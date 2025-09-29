from django.contrib.auth.models import AbstractUser  # type: ignore
from django.db import models  # type: ignore


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('client', 'Client'),
        ('manager', 'Manager'),
        ('delivery_man', 'Delivery_man'),
    )
    telefone = models.CharField(max_length=20, blank=True)
    endereco = models.CharField(max_length=255, blank=True)
    cpf = models.CharField(max_length=14, blank=True)
    nome = models.CharField(max_length=100, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    foto_perfil = models.ImageField(upload_to='perfil/', blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
