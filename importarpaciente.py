
import datetime
from pacientes.models import Paciente
from stores import exec_sqlstring

def revertirfecha(fecha):
    fecha_formato = '%d/%m/%Y'
    fecha_obj = datetime.datetime.strptime(fecha, fecha_formato)
    return fecha_obj

pacientes = exec_sqlstring()

lista = list()

i = 0

for paciente in pacientes:
    idpaciente = paciente[0]
    apellido = paciente[1]
    nombre = paciente[2]
    numerodocumento = paciente[3]
    fechanacimiento = revertirfecha(paciente[4])
    sexo = paciente[5]
    pais = paciente[6]
    provincia = paciente[7]
    partido = paciente[8]
    localidad = paciente[9]
    barrio = paciente[10]
    domicilio = paciente[11]

    tupla = (
        idpaciente, apellido, nombre, numerodocumento, fechanacimiento,
        sexo, pais, provincia, partido, localidad, barrio, domicilio
    )

    #lista.append(tupla)

    for t in tupla:
        if i < 1000:
            try:
                consulta = Paciente.objects.get(idsigho=idpaciente)
            except:
                paciente = Paciente(
                    idsigho=idpaciente,
                    apellido=apellido,
                    nombre=nombre,
                    numerodocumento=numerodocumento,
                    fechanacimiento=fechanacimiento,
                    sexo=sexo,
                    pais=pais,
                    provincia=provincia,
                    partido=partido,
                    localidad=localidad,
                    barrio=barrio,
                    domicilio=domicilio
                    )
                paciente.save()
                i = i + 1
    tupla = None

"""
def grabarpersona(dataset):
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()
    cursor.executemany(
        'INSERT INTO paciente(idpaciente, apellido, nombre, numerodocumento, fechanacimiento, sexo, pais, provincia, partido, localidad, barrio, domicilio) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', dataset)
    conexion.commit()
    conexion.close()

grabarpersona(lista)
"""




