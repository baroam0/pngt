from django.contrib import admin

from .models import Unidad, Medicamento, EntregaMedicamento

admin.site.register(Unidad)
admin.site.register(Medicamento)
admin.site.register(EntregaMedicamento)

# Register your models here.
