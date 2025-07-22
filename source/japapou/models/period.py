from django.db import models  # type: ignore
from .menu import Menu


class Period(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = "Período"
        verbose_name_plural = "Períodos"

    def __str__(self):
        return f"{self.menu.name}: {self.start_date.strftime('%d/%m/%Y')} - {self.end_date.strftime('%d/%m/%Y')}"
