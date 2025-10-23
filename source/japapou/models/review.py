from django.db import models  # type: ignore
from django.conf import settings # type: ignore
from .user import CustomUser
from .plate import Plate

class Review(models.Model):
    '''
        classe base de avaliacao
    '''
    NOTA_CHOICES = (
        (1, '1 Estrela'),
        (2, '2 Estrelas'),
        (3, '3 Estrelas'),
        (4, '4 Estrelas'),
        (5, '5 Estrelas'),
    )

    value = models.IntegerField(choices=NOTA_CHOICES, default=5, verbose_name="Nota")
    comment = models.TextField(null=False, blank=False, max_length=500, verbose_name="Comentário")
    
    created_at = models.DateTimeField(auto_now_add=True)

    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        abstract = True
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Nota: {self.value} por {self.usuario.username}"


class PlateReview(Review):
    '''
        classe de avaliacao de prato
    '''
    image_review = models.ImageField(upload_to="PlateReview/", null=True, blank=True)

    plate = models.ForeignKey(
        Plate, 
        on_delete=models.CASCADE, 
        related_name="avaliacoes_pratos",
    )

    class Meta:
        verbose_name = "Avaliação de Prato"
        verbose_name_plural = "Avaliações de Pratos"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'plate'],
                name='unique_user_plate_review'
            )
        ]

    def __str__(self):
        return f"{self.usuario} ({self.value}/5) {self.plate.name}"
    
class CourierReview(Review):
    '''
        classe de avaliacao de entregador
    '''

    entregador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="avaliacoes_recebidas",
        limit_choices_to={'tipo_usuario': 'DELIVERY_MAN'}
    )

    class Meta:
        verbose_name = "Avaliação de Entregador"
        verbose_name_plural = "Avaliações de Entregador"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'entregador'],
                name='unique_user_courier_review'
            )
        ]

    def __str__(self):
        return f"Avaliação de {self.entregador.username} por {self.usuario.username} ({self.value}/5)"
