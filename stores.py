
import json
import pyodbc, time, requests


def exec_sqlstring():
    '''
    returna todos los registros para recorrer por medio de un string
    '''
    base_url = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=10.10.0.79;DATABASE=MHO;UID=tableroCovid;PWD=C0ntrolCov2020'

    sp = "select p.PacienteID, p.Apellido , p.nombre, p.NumeroDocumento, convert(varchar(10),p.FechaNacimiento,103) FechaNacimiento, case when p.Sexoid =1 then 'masculino' else 'femenino' end 'Sexo', isnull(Ps.Descripcion,'') AS 'Pais', isnull(Prov.Descripcion,'') AS 'Provincia', isnull(Par.Descripcion,'') AS 'Partido', isnull(Lo.Descripcion,'') AS 'Localidad', isnull(Ba.Descripcion,'') AS 'Barrio', isnull(P.Domicilio,'') AS 'Domicilio' from paciente P LEFT JOIN Pais Ps ON Ps.PaisID = P.PaisID LEFT JOIN Provincia Prov ON P.ProvinciaID = Prov.ProvinciaID AND Prov.PaisID = Ps.PaisID LEFT JOIN Partido Par ON P.PartidoID = Par.PartidoID AND Par.PaisID = Ps.PaisID AND Par.ProvinciaID = Prov.ProvinciaID LEFT JOIN Localidad Lo ON P.LocalidadID = Lo.LocalidadID AND Lo.PaisID = P.PaisID AND Lo.ProvinciaID = Prov.ProvinciaID AND Lo.PartidoID = Par.PartidoID LEFT JOIN Barrio Ba ON P.BarrioID = Ba.BarrioID AND Ba.PaisID = Ps.PaisID AND Ba.ProvinciaID = Prov.ProvinciaID AND Ba.PartidoID = Par.PartidoID AND BA.LocalidadID = Lo.LocalidadID where (NumeroDocumento  is not  null) or (NumeroDocumento <> 0)or  (p.Apellido <>' ' ) group by p.PacienteID, p.Apellido , p.nombre, p.NumeroDocumento, convert(varchar(10),p.FechaNacimiento,103) , case when p.Sexoid =1 then 'masculino' else 'femenino' end , isnull(Ps.Descripcion,'') , isnull(Prov.Descripcion,'') , isnull(Par.Descripcion,'') , isnull(Lo.Descripcion,'') , isnull(Ba.Descripcion,''), isnull(P.Domicilio,'') order by p.Apellido"

    row = []
    try:
        cnxn = pyodbc.connect(base_url)
        cursor = cnxn.cursor() # Create a cursor from the connection
        cursor.execute(sp)
        row = cursor.fetchall()
        cursor.close()
        cnxn.close()
        return row
    except Exception as e:
        print(str(e), sp)

