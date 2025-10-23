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
    image_review = models.ImageField(null=True, blank=True, verbose_name="Foto do prato")
    comment = models.TextField(null=False, blank=False, max_length=500, verbose_name="Comentário")
    
    created_at = models.DateTimeField(auto_now_add=True)

    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        ordering = ["-created-at"]

    def __str__(self):
        return f"Rating: {self.value} - {self.created_at} \n {self.comment}"


class PlateReview(Review):
    '''
        classe de avaliacao de prato
    '''
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="PlateReview/", null=True, blank=True)

    class Meta:
        verbose_name = "Avaliação de Prato"
        verbose_name_plural = "Avaliações de Pratos"

        unique_together = ('plate', 'avaliador')

    def __str__(self):
        return f"{self.title} ({self.value}/5)"
    
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

        unique_together = ('entregador_avaliado', 'avaliador')

    def __str__(self):
        return f"Avaliação de {self.entregador_avaliado.username} por {self.avaliador.username} ({self.value}/5)"
