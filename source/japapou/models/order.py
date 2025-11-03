from django.db import models  # type: ignore
from django.conf import settings # type: ignore # Importar settings

class Order(models.Model):
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT, 
        related_name="pedidos"
    )


    date = models.DateField(auto_now_add=True) # Alterado para auto_now_add
    estimate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # Permitir nulo
    total = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    altered_at = models.DateTimeField(auto_now=True)
    
  