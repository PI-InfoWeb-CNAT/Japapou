from django.db import models  # type: ignore
from .plate import Plate


class Menu(models.Model):
    name = models.CharField(null=False, max_length=100)
    plates = models.ManyToManyField(Plate, blank=True)

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"

    def __str__(self):
        return f"{self.name}: {self.plates.count()} pratos"
