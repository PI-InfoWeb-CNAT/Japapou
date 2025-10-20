from django.contrib.auth.models import AbstractUser  # type: ignore
from django.db import models  # type: ignore


class CustomUser(AbstractUser):

    class TipoUsuario(models.TextChoices):
        # herdar de models.textchoices para criar uma lista de opções
        CLIENT = 'CLIENT', 'Client'
        DELIVERY_MAN = 'DELIVERY_MAN', 'Delivery_man'
        MANAGER = 'MANAGER', 'Manager'

    # Campo para definir a identidade principal do usuário
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TipoUsuario.choices, # gera uma lista de tuplas que é o formato que o django espera para o menu dropdown
        default=TipoUsuario.MANAGER, 
        null=True,
        blank=True
    )


    # AbstractUser já tem username, email, password, first_name, last_name, etc.
    telefone = models.CharField(max_length=20, blank=True)
    endereco = models.CharField(max_length=255, blank=True)
    cpf = models.CharField(max_length=14, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    foto_perfil = models.ImageField(upload_to='perfil/', blank=True, null=True)
    cnh = models.CharField(max_length=10, blank=True)
    modelo_moto = models.CharField(max_length=20, blank=True)
    cor_moto = models.CharField(max_length=10, blank=True)
    placa_moto = models.CharField(max_length=10, blank=True)
    foto = models.ImageField(blank=True, null=True, upload_to="fotos/")
