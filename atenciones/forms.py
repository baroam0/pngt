
from django import forms
from django.contrib.auth.models import User

from .models import Atencion, Especialidad
from pacientes.models import Paciente


class AtencionForm(forms.ModelForm):
    paciente = forms.ModelChoiceField(
        label="Paciente", queryset=Paciente.objects.all(), required=True)
    especialidad = forms.ModelChoiceField(
        label="Especialidad",
        queryset=Especialidad.objects.all(),
        required=True
    )
    
    def __init__(self, *args, **kwargs):
        super(AtencionForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Atencion
        fields = ['paciente', 'especialidad']


class EspecialidadForm(forms.ModelForm):
    descripcion = forms.CharField(
        label="Descripcion", required=True)

    def __init__(self, *args, **kwargs):
        super(EspecialidadForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Especialidad
        fields = ['descripcion']
