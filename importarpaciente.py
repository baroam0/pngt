
import csv
import datetime
from pacientes.models import Paciente
from stores import exec_sqlstring

def revertirfecha(fecha):
    fecha_formato = '%d/%m/%Y'
    fecha_obj = datetime.datetime.strptime(fecha, fecha_formato)
    return fecha_obj

#pacientes = exec_sqlstring()
# opening the CSV file
with open('padron.csv', mode ='r', encoding="utf-8") as file:
    csvFile = csv.reader(file)
    
    for elemento in csvFile:
        
        try:
            print(elemento[0])
            lines = elemento[0].split(";")
            numerodocumento = lines[0]
            apellido = lines[2]
            nombre = lines[3]
            domicilio = lines[4]
            if lines[6] == "M":
                sexo = "Masculino"
            else:
                sexo = "Femenino"
            provincia = "Formosa"
            departamento = lines[7]
            localidad = lines[9]

            paciente = Paciente(
                numerodocumento=numerodocumento,
                apellido=apellido,
                nombre=nombre,
                domicilio=domicilio, sexo=sexo,
                provincia=provincia,
                partido=departamento,
                localidad=localidad)
            paciente.save()
        except:
            pass


"""
for a in listciudadanos:
    list_a = a.split(";")
    
    apellido = list_a[1]
    nombre = list_a[2]
    numerodocumento = list_a[0]
    fechanacimiento = revertirfecha(paciente[4])
    if 
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


def grabarpersona(dataset):
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()
    cursor.executemany(
        'INSERT INTO paciente(idpaciente, apellido, nombre, numerodocumento, fechanacimiento, sexo, pais, provincia, partido, localidad, barrio, domicilio) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', dataset)
    conexion.commit()
    conexion.close()

grabarpersona(lista)
"""

