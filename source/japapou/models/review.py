from django.db import models  # type: ignore


class Review(models.Model):
    value = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    comment = models.CharField(null=True, max_length=500)

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        ordering = ["-date"]

    def __str__(self):
        return f"Rating: {self.value} - {self.created_at} \n {self.comment}"

class PlateReview(Rating):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="PlateReview/", null=True, blank=True)

    class Meta:
        verbose_name = "Avaliação de Prato"
        verbose_name_plural = "Avaliações de Pratos"

    def __str__(self):
        return f"{self.title} ({self.value}/5)"
    
class CourierReview(Review):
    class Meta:
        verbose_name = "Avaliação de Entregador"
        verbose_name_plural = "Avaliações de Entregador"

    def __str__(self):
        return f"Entregador avaliado em {self.value}/5"
