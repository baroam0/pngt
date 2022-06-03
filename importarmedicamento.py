
from medicamentos.models import Medicamento, Unidad

archivo = open("medicamentos.txt", "r")

medicamentos = archivo.readlines()

medicamentos = list(dict.fromkeys(medicamentos))

print("Grabando...")

idunidad = Unidad.objects.get(descripcion="Unidad")

for medicamento in medicamentos:
    if medicamento != "":
        grabar = Medicamento(descripcion=str(medicamento), unidad=idunidad, cantidad=0 )
        grabar.save()

