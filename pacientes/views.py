
from django.contrib import messages
from django.core.paginator import Paginator
from django.http.response import JsonResponse

from django.shortcuts import render, redirect

from django.db.models import Q
from .forms import PacienteForm
from .models import Paciente


def verifica_paciente(numero_documento):
    """Funcion para verificar si existe un paciente con ese dni
    """
    try:
        consulta = Paciente.objects.get(numerodocumento=numero_documento)
        existe = True
    except:
        existe = False

    return existe


def listadopaciente(request):

    if "txtBuscar" in request.GET:
        parametro = request.GET.get("txtBuscar")

        if parametro == "":
            consulta = Paciente.objects.all().order_by('apellido')
        else:
            if '"' in parametro:
                if "    " in parametro:
                    listparametro = parametro.split('"')
                    nrodocumento = listparametro[1]
                    nrodocumento = nrodocumento.replace("    ", "")
                    consulta = Paciente.objects.filter(
                        numerodocumento=nrodocumento
                    ).order_by('apellido')
                    parametro = nrodocumento
                else:
                    listparametro = parametro.split('"')
                    nrodocumento = listparametro[4]
                    consulta = Paciente.objects.filter(
                        numerodocumento=nrodocumento
                    ).order_by('apellido')
                    parametro = nrodocumento
            else:
                consulta = Paciente.objects.filter(
                    Q(apellido__icontains=parametro) |
                    Q(nombre__icontains=parametro) |
                    Q(ayn__icontains=parametro) |
                    Q(numerodocumento__icontains=parametro)
                ).order_by('apellido')
        if not consulta:
            return redirect('/pacientenuevopreload/' + request.GET.get("txtBuscar"))   

    else:
        parametro = None
        consulta = Paciente.objects.all().order_by('apellido')

    paginador = Paginator(consulta, 15)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1

    resultados = paginador.get_page(page)
    if parametro:
        return render(
            request,
            'pacientes/paciente_list.html',
            {
                'resultados': resultados,
                'parametro': parametro
            }
        )
    else:
        return render(request, 'pacientes/paciente_list.html', {'resultados': resultados})



def nuevopacientepreload(request, rawdata):

    if request.POST:
        form = PacienteForm(request.POST)
        existe = verifica_paciente(request.POST['numerodocumento'])
        if existe == True:
            messages.error(request, "EL PACIENTE YA EXISTE EN LOS REGISTROS")
            return redirect('/pacientelistado')
        else:
            if form.is_valid():
                form.save()
                consulta = Paciente.objects.latest('pk')
                messages.success(
                    request,
                    "SE HAN GUARDADO LOS DATOS DEL PACIENTE " + str(consulta.apellido).upper() + ', ' + str(consulta.nombre).upper())
                #return redirect('/pacienteeditar/' + str(consulta.pk))
                return redirect('/pacientelistado/?txtBuscar=' + str(consulta.numerodocumento))
            else:
                return render(
                    request,
                    'pacientes/paciente_nuevo.html',
                    {
                        "form": form,
                    })
    else:
        if "    " in rawdata:
            listrawdata = rawdata.split('"')
            data = dict()
            data['apellido'] = listrawdata[4]
            data['nombre'] = listrawdata[5]
            if listrawdata[8] == "M":
                data['sexo'] = "Masculino"
            else:
                data['sexo'] = "Femenino"
            data['numerodocumento'] = listrawdata[1]
            data['fechanacimiento'] = listrawdata[7]
            data['pais'] = listrawdata[6]

            form = PacienteForm(data)
            return render(
                request,
                'pacientes/paciente_nuevo.html',
                {
                    "form": form,
                }
            )
        else:
            if '"' in rawdata:
                listrawdata = rawdata.split('"')
                data = dict()
                data['apellido'] = listrawdata[1]
                data['nombre'] = listrawdata[2]
                if listrawdata[3] == "M":
                    data['sexo'] = "Masculino"
                else:
                    data['sexo'] = "Femenino"
                data['numerodocumento'] = listrawdata[4]
                data['fechanacimiento'] = listrawdata[6].replace("-","/")

                form = PacienteForm(data)
                return render(
                    request,
                    'pacientes/paciente_nuevo.html',
                    {
                        "form": form,
                    }
                )
            else:
                form = PacienteForm()
                return render(
                    request,
                    'pacientes/paciente_nuevo.html',
                    {
                        "form": form,
                    }
                )


def nuevopaciente(request):
    if request.POST:
        form = PacienteForm(request.POST)
        existe = verifica_paciente(request.POST['numerodocumento'])
        if existe == True:
            messages.error(request, "EL PACIENTE YA EXISTE EN LOS REGISTROS")
            return redirect('/pacientelistado')
        else:
            if form.is_valid():
                form.save()
                consulta = Paciente.objects.latest('pk')
                messages.success(
                    request,
                    "SE HAN GUARDADO LOS DATOS DEL PACIENTE " + str(consulta.apellido).upper() + ', ' + str(consulta.nombre).upper())
                #return redirect('/pacienteeditar/' + str(consulta.pk))
                return redirect('/pacientelistado')
            else:
                return render(
                    request,
                    'pacientes/paciente_nuevo.html',
                    {
                        "form": form,
                    })
    else:
        form = PacienteForm()
        return render(
            request,
            'pacientes/paciente_nuevo.html',
            {
                "form": form,
            }
        )


def editarpaciente(request, pk):
    consulta = Paciente.objects.get(pk=pk)
    
    if request.POST:
        form = PacienteForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, "SE HA MOFICICADO EL PACIENTE")
            #return redirect('/pacientelistado')
            return redirect('/pacientelistado/?txtBuscar=' + str(consulta.numerodocumento))
        else:
            return render(request, "pacientes/paciente_nuevo.html", {"form": form})
    else:
        form = PacienteForm(instance=consulta)

        return render(
            request,
            'pacientes/paciente_nuevo.html',
            {
                "form": form,    
                "paciente": consulta.pk,
            }
        )


def ajaxpaciente(request):
    parametro = request.GET.get('term')

    consulta = Paciente.objects.filter(
        ayn__icontains=parametro
    )

    dict_tmp = dict()
    list_tmp = list()

    if len(consulta) > 0:
        for i in consulta:
            dict_tmp["id"] = i.pk
            dict_tmp["text"] = i.apellido.upper() + " " + i.nombre.upper()
            list_tmp.append(dict_tmp)
            dict_tmp = dict()

    return JsonResponse(list_tmp, safe=False)

            

# Create your views here.
