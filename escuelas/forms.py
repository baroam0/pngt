
from django import forms
from django.contrib.auth.models import User

from .models import Escuela
from pacientes.models import Paciente


class EscuelaForm(forms.ModelForm):
    descripcion = forms.CharField(
        label="Descripcion", required=True)
    
    operativo = forms.BooleanField(label="Operativo", required=False)
    
    def __init__(self, *args, **kwargs):
        super(EscuelaForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            if field != "operativo":
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })

    class Meta:
        model = Escuela
        fields = ['descripcion', 'operativo']

