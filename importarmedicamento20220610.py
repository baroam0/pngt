
from medicamentos.models import Medicamento, Unidad

archivo = open("medicamentos20220610.txt", "r")

medicamentos = archivo.readlines()

medicamentos = list(dict.fromkeys(medicamentos))

print("Grabando...")

idunidad = Unidad.objects.get(descripcion="Unidad")

for medicamento in medicamentos:
    arraymedicamento = medicamento.split(";")

    print(arraymedicamento[0])
    print(arraymedicamento[1])

    if medicamento != "":
        grabar = Medicamento(
            descripcion=str(arraymedicamento[0]),
            unidad=idunidad,
            cantidad=int(arraymedicamento[1])
        )
        grabar.save()

