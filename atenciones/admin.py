from lib2to3.pgen2.token import ATEQUAL
from django.contrib import admin

from .models import Especialidad, Atencion

admin.site.register(Especialidad)
admin.site.register(Atencion)

# Register your models here.
