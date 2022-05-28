


from pacientes.models import Paciente
from stores import exec_sqlstring


pacientes = Paciente.objects.all()


for paciente in pacientes:
    ayn = paciente.apellido + " " + paciente.nombre
    paciente.ayn=ayn
    paciente.save()

