
from django import forms
from django.contrib.auth.models import User

from.models import Medicamento, Unidad, Receta, RecetaDetalle, EntregaMedicamento
from pacientes.models import Paciente


class MedicamentoForm(forms.ModelForm):
    descripcion = forms.CharField(
        label="Descripcion(*)", required=True)
    cantidad = forms.IntegerField(label="Cantidad(*)", required=True)
    unidad = forms.ModelChoiceField(
        queryset=Unidad.objects.all(), label="Unidad(*)", required=True)

    def __init__(self, *args, **kwargs):
        super(MedicamentoForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Medicamento
        fields = ['descripcion', 'unidad', 'cantidad']


class RecetaForm(forms.ModelForm):
    medicamento = forms.ModelChoiceField(
        queryset=Medicamento.objects.all(), label="Medicamento(*)", required=True)

    def __init__(self, *args, **kwargs):
        super(RecetaForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Receta
        fields = ['paciente']



class RecetaDetalleForm(forms.ModelForm):

    medicamento = forms.ModelChoiceField(
        queryset=Medicamento.objects.all().order_by("descripcion"), label="Medicamentos"
    )
    cantidad = forms.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        super(RecetaDetalleForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = RecetaDetalle
        fields = ['medicamento', 'cantidad']
        exclude = ['paciente']


class EntregaMedicamentoForm(forms.ModelForm):
    medicamento = forms.ModelChoiceField(
        queryset=Medicamento.objects.all(),
        label="Medicamento(*)",
        required=True
    )
    cantidad = forms.IntegerField(label="Cantidad(*)", required=True)

    def __init__(self, *args, **kwargs):
        super(EntregaMedicamentoForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = EntregaMedicamento
        fields = ['medicamento', 'cantidad']