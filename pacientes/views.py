
from django.contrib import messages
from django.core.paginator import Paginator
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
            consulta = Paciente.objects.filter(
                Q(apellido__icontains=parametro) |
                Q(nombre__contains=parametro) |
                Q(numerodocumento__contains=parametro)
            ).order_by('apellido')
    else:
        consulta = Paciente.objects.all().order_by('apellido')

    paginador = Paginator(consulta, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1

    resultados = paginador.get_page(page)
    return render(request, 'pacientes/paciente_list.html', {'resultados': resultados})



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
            return redirect('/pacientelistado')
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
        
            

# Create your views here.
