from django.db import models  # type: ignore

class Prato(models.Model):
    name = models.CharField(null=False, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    altered_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.name)