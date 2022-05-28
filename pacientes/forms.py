
from django import forms
from django.contrib.auth.models import User

from .models import Paciente


class PacienteForm(forms.ModelForm):

    SEX_CHOICES = [
        ("Masculino", "Masculino"),
        ("Femenino", "Femenino")
    ]

    PAIS_CHOICES = [
        ("Argentina", "Argentina"),
        ("Bolivia", "Bolivia"),
        ("Colombia", "Colombia"),
        ("Paraguay", "Paraguay"),
        ("Venezuela", "Venezuela")
    ]

    nombre = forms.CharField(label="Nombre", required=True)
    apellido = forms.CharField(label="Apellido", required=True)
    numerodocumento = forms.CharField(label="Numero Documento", required=True)

    sexo = forms.ChoiceField(required=False, choices=SEX_CHOICES)
    
    fechanacimiento = forms.DateField(
        label="Fecha Nacimiento", required=False)

    pais = forms.ChoiceField(required=False, label="Pais", choices=PAIS_CHOICES)
    provincia = forms.CharField(label="Provincia", required=False)
    localidad = forms.CharField(label="Localidad", required=False)
    barrio = forms.CharField(label="Barrio", required=False)
    domicilio = forms.CharField(label="Domicilio", required=False)

    def __init__(self, *args, **kwargs):
        super(PacienteForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Paciente
        fields = ['nombre', 'apellido', 'numerodocumento', 'sexo',
            'fechanacimiento', 'pais', 'provincia','localidad',
            'barrio','domicilio'
            ]
        exclude = ['ayn']
