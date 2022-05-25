from django.db import models


class Paciente(models.Model):
    SEX_CHOICES = [
        ("masculino", "masculino"),
        ("femenino", "femenino")
    ]

    idsigho = models.CharField(max_length=100, null=True, blank=True)
    apellido = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100) 
    numerodocumento = models.CharField(max_length=100)
    fechanacimiento = models.DateField(null=True, blank=True)
    sexo = models.CharField(
        max_length=9,
        choices=SEX_CHOICES,
        default="masculino",
    )
    pais = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    partido = models.CharField(max_length=100)
    localidad = models.CharField(max_length=100)
    barrio = models.CharField(max_length=100)
    domicilio = models.CharField(max_length=100)

    def __str__(self):
        return self.apellido + ", " + self.nombre

    class Meta:
        verbose_name_plural = "Pacientes"


# Create your models here.
