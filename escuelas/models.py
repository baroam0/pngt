
from django.db import models


class Escuela(models.Model):
    descripcion = models.CharField(
        max_length=100, unique=True, blank=False, null=False)
    operativo = models.BooleanField(default=False)
    
    def __str__(self):
        return self.descripcion

    """
    def save(self,*args, **kwargs):

        if self.operativo==True:
            escuelas = Escuela.objects.all()
            for escuela in escuelas:
                escuela.operativo = False
                escuela.save()
            super(Escuela, self).save(*args, **kwargs)
    """
    class Meta:
        verbose_name_plural = "Escuelas"


# Create your models here.
