
from django.db import models

from escuelas.models import Escuela
from pacientes.models import Paciente


class Unidad(models.Model):
    descripcion = models.CharField(
        max_length=100, unique=True, blank=False, null=False)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Unidades de Medicamentos"


class PresentacionMedica(models.Model):
    descripcion = models.CharField(
        max_length=100, unique=True, blank=False, null=False)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Presentaciones Medicas"


class Medicamento(models.Model):
    descripcion = models.CharField(
        max_length=100, unique=True, blank=False, null=False)
    cantidad = models.IntegerField()
    unidad = models.ForeignKey(
        Unidad, default=1, on_delete=models.CASCADE)

    presentacion = models.ForeignKey(
        PresentacionMedica,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Medicamentos"


class Receta(models.Model):
    fecha = models.DateTimeField(auto_now=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    escuela = models.ForeignKey(
        Escuela, blank=False, null=False, default=1,
        on_delete=models.CASCADE)

    def __str__(self):
        return str(self.fecha)

    def save(self,*args, **kwargs):
        consultaescuela = Escuela.objects.get(operativo=True)
        self.escuela=consultaescuela
        super(Receta, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Recetas"


class RecetaDetalle(models.Model):
    receta = models.ForeignKey(
        Receta, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(
        Medicamento, blank=False, null=False, default=1,
        on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)

    def __str__(self):
        return str(self.fecha)

    class Meta:
        verbose_name_plural = "Detalles Recetas"


class EntregaMedicamento(models.Model):
    fecha = models.DateTimeField(auto_now=True)
    fecha_formulario = models.DateField(null=True, blank=True)
    medicamento = models.ForeignKey(
        Medicamento, on_delete=models.CASCADE)
    cantidad = models.IntegerField(
        null=False, blank=False)
    escuela = models.ForeignKey(
        Escuela, blank=False, null=False, default=1,
        on_delete=models.CASCADE)

    def __str__(self):
        return str(self.fecha)

    def save(self,*args, **kwargs):
        consultaescuela = Escuela.objects.get(operativo=True)
        self.escuela=consultaescuela
        super(EntregaMedicamento, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Entregas de Medicamentos"


class RecepcionaMedicamento(models.Model):
    fecha = models.DateTimeField(auto_now=True)
    fecha_formulario = models.DateField(null=True, blank=True)
    medicamento = models.ForeignKey(
        Medicamento, null=True, blank=True, on_delete=models.CASCADE)
    cantidad = models.IntegerField(
        null=False, blank=False)

    def __str__(self):
        return str(self.fecha)

    class Meta:
        verbose_name_plural = "Recepciones de Medicamentos"


# Create your models here.
