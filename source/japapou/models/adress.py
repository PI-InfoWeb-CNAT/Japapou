from django.db import models # type: ignore
from django.conf import settings # type: ignore


class Endereco(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enderecos" # Permite usar request.user.enderecos.all()
    )
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=20)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100, default="São Paulo") # Exemplo
    estado = models.CharField(max_length=2, default="SP") # Exemplo
    cep = models.CharField(max_length=9) # Formato '00000-000'
    
    # Um "apelido" para o endereço, ex: "Casa", "Trabalho"
    apelido = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    def __str__(self):
        # Retorna o endereço formatado
        return f"{self.logradouro}, {self.numero} - {self.bairro}, {self.cidade}"