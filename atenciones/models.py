
from django.db import models

from escuelas.models import Escuela
from pacientes.models import Paciente


class Especialidad(models.Model):
    descripcion = models.CharField(max_length=100, unique=True)
    predeterminada = models.BooleanField(default=False)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Especialidades"


class Atencion(models.Model):
    fecha = models.DateTimeField(auto_now=True)
    #fecha = models.DateField(auto_now=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    especialidad = models.ForeignKey(
        Especialidad, blank=False, null=False,
        default=1,
        on_delete=models.CASCADE
    )
    escuela = models.ForeignKey(
        Escuela, blank=False, null=False, default=1, 
        on_delete=models.CASCADE)

    def __str__(self):
        return str(self.fecha)
    
    def save(self,*args, **kwargs):
        consultaescuela = Escuela.objects.get(operativo=True)
        self.escuela=consultaescuela
        super(Atencion, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Atenciones"


# Create your models here.
