
from datetime import datetime
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, QuerySet
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt


from escuelas.models import Escuela
from pacientes.models import Paciente

from .forms import AtencionForm, EspecialidadForm, AtencionLinkForm
from .models import Atencion, Especialidad


def listadoatenciones(request):
    escueladefault = Escuela.objects.get(operativo=True)
    if "txtBuscar" in request.GET:
        parametro = request.GET.get("txtBuscar")
        if parametro == "":
            #consulta = Atencion.objects.all().order_by('pk')
            consulta = Atencion.objects.filter(escuela=escueladefault.pk).order_by('-fecha')
        else:
            if parametro.isnumeric():
                idatencion = int(parametro)
            else:
                idatencion = None
            consulta = Atencion.objects.filter(
                Q(pk=idatencion) |
                Q(paciente__apellido__icontains=parametro) |
                Q(paciente__nombre__contains=parametro) |
                Q(paciente__numerodocumento__contains=parametro) &
                Q(escuela=escueladefault.pk)
            ).order_by('-fecha')
    else:
        consulta = Atencion.objects.filter(escuela=escueladefault.pk).order_by('-fecha')

    paginador = Paginator(consulta, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1

    resultados = paginador.get_page(page)
    return render(request, 'atenciones/atencion_list.html', {'resultados': resultados})


def nuevaatencion(request):
    especialidades = Especialidad.objects.all()
    print(especialidades)
    if request.POST:
        form = AtencionForm(request.POST)

        if form.is_valid():
            form.save()
            consulta = Atencion.objects.latest('pk')
            messages.success(
                request,
                "SE HAN GUARDADO LOS DATOS DE LA ATENCION")
                #return redirect('/pacienteeditar/' + str(consulta.pk))
            return redirect('/atencioneslistado/?txtBuscar=', str(consulta.pk))
        else:
            return render(
                request,
                'atenciones/atencion_link.html',
                {
                    "form": form,
                    "especialidades": especialidades
                })
    else:
        form = AtencionForm()
        return render(
            request,
            'atenciones/atencion_link.html',
            {
                "form": form,
                "especialidades": especialidades
            }
        )


def editaratencion(request, pk):
    consulta = Atencion.objects.get(pk=pk)
    paciente = Paciente.objects.filter(pk=consulta.paciente.pk)
    especialidad = Especialidad.objects.get(pk=consulta.especialidad.pk)
    especialidades = Especialidad.objects.all()
    
    if request.POST:
        form = AtencionLinkForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, "SE HA MOFICICADO LA ATENCION")
            return redirect('/atencioneslistado')
        else:
            return render(request, "atenciones/atencion_link.html", {"form": form, "paciente": paciente})
    else:
        form = AtencionLinkForm(instance=consulta)

        return render(
            request,
            'atenciones/atencion_link.html',
            {
                "form": form,
                "paciente": paciente,
                "especialidadupdate": especialidad,
                "especialidades": especialidades
            }
        )


def listadoespecialidades(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get("txtBuscar")
        if parametro == "":    
            consulta = Especialidad.objects.all().order_by('descripcion')
        else:
            consulta = Especialidad.objects.filter(
                descripcion__icontains=parametro).order_by('descripcion')
    else:
        consulta = Especialidad.objects.all().order_by('pk')

    paginador = Paginator(consulta, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1

    resultados = paginador.get_page(page)
    return render(request, 'atenciones/especialidad_list.html', {'resultados': resultados})


def nuevaespecialidad(request):
    if request.POST:
        form = EspecialidadForm(request.POST)
        if form.is_valid():
            form.save()
            consulta = Especialidad.objects.latest('pk')
            if consulta.predeterminada == True:
                especialidades = Especialidad.objects.all().exclude(pk=consulta.pk)
                for especialidad in especialidades:
                    especialidad.predeterminada = False
                    especialidad.save()

            messages.success(
                request,
                "SE HAN GUARDADO DE LA ESEPECIALIDAD")
                #return redirect('/pacienteeditar/' + str(consulta.pk))
            return redirect('/practicaslistado')
        else:
            return render(
                request,
                'atenciones/especialidad_nuevo.html',
                {
                    "form": form,
                })
    else:
        form = EspecialidadForm()
        return render(
            request,
            'atenciones/especialidad_nuevo.html',
            {
                "form": form,
            }
        )


def editarespecialidad(request, pk):
    consulta = Especialidad.objects.get(pk=pk)
    
    if request.POST:
        form = EspecialidadForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            
            if consulta.predeterminada == True:
                especialidades = Especialidad.objects.all().exclude(pk=consulta.pk)
                for e in especialidades:
                    e.predeterminada = False
                    e.save()
            
            messages.success(request, "SE HA MOFICICADO LA ESPECIALIDAD")
            return redirect('/practicaslistado')
        else:
            return render(request, "atenciones/especialidad_nuevo.html", {"form": form})
    else:
        form = EspecialidadForm(instance=consulta)

        return render(
            request,
            'atenciones/especialidad_nuevo.html',
            {
                "form": form,
            }
        )


def atencionporescuela(request):
    escuelas = Escuela.objects.all()
    return render(
        request, 'atenciones/atencionporescuela.html', {'escuelas': escuelas})


def ajaxgraficoatencionporescuela(request):
    if request.method=="GET":
        escuela = Escuela.objects.get(pk=request.GET.get("escuela"))
        practicas = list()
        cantidades = list()
        results = (
            Atencion.objects.filter(escuela=escuela.pk).values('especialidad').annotate(dcount=Count('especialidad')).order_by()
        )

        for result in results:
            especialidad = Especialidad.objects.get(pk=result["especialidad"]) 
            practicas.append(especialidad.descripcion.upper())
            cantidades.append(result["dcount"])

        data = {
            "practicas": practicas,
            "cantidades": cantidades,
            "escuela": escuela.descripcion.upper()
        }        

        return JsonResponse(data, safe=False)


def renderticket(request, pk):
    if request.method=="GET":
        atencion = Atencion.objects.get(pk=pk)

        return render(
            request, 'atenciones/ticket.html', {'atencion': atencion})


def nuevaatencionlink(request, pk):
    paciente = Paciente.objects.filter(pk=pk)
    especialidad = Especialidad.objects.all()
    

    if request.POST:
        form = AtencionLinkForm(request.POST)
        if form.is_valid():
            form.save()
            consulta = Atencion.objects.latest('pk')
            messages.success(
                request,
                "SE HAN GUARDADO LOS DATOS DE LA ATENCION")
                #return redirect('/pacienteeditar/' + str(consulta.pk))
            return redirect('/atencioneslistado/?txtBuscar=', str(consulta.pk))
        else:
            return render(
                request,
                'atenciones/atencion_link.html',
                {
                    "form": form,
                    "paciente": paciente,
                    "especialidades": especialidad
                })
    else:
        form = AtencionLinkForm()
        return render(
            request,
            'atenciones/atencion_link.html',
            {
                "form": form,
                "paciente": paciente,
                "especialidades": especialidad
            }
        )


def ajaxconsultaatencion(request):
    if request.is_ajax and request.method == "GET":
        escuela = Escuela.objects.get(operativo=True)
        idespecialidad = request.GET.get("especialidad", None)
        idpaciente = request.GET.get("paciente", None)
        
        especialidad = Especialidad.objects.get(pk=int(idespecialidad))
        paciente = Paciente.objects.get(pk=int(idpaciente))
        
        try:
            atencion = Atencion.objects.filter(
                paciente=paciente.pk,
                especialidad=especialidad.pk,
                escuela=escuela) 
        except Atencion.DoesNotExist:
            atencion = None
        
        if atencion:
            return JsonResponse({"existe":1}, status = 200)
        else:
            return JsonResponse({"existe":0}, status = 200)


@csrf_exempt
def ajaxgrabaratencioneimprimir(request):
    if request.is_ajax and request.method == "POST":
        idespecialidad = request.POST.get("especialidad", None)
        idpaciente = request.POST.get("paciente", None)
        
        especialidad = Especialidad.objects.get(pk=int(idespecialidad))
        paciente = Paciente.objects.get(pk=int(idpaciente))
        escuela = Escuela.objects.get(operativo=True)

        atencion = Atencion(paciente=paciente,especialidad=especialidad,escuela=escuela)
        atencion.save()
        atencion = Atencion.objects.latest('pk')

        return JsonResponse({"atencion": atencion.pk}, status = 200)


def ajaxeliminaratencion(request):
    if request.is_ajax and request.method == "GET":
        idatencion = request.GET.get("atencion", None)
        atencion = Atencion.objects.get(pk=int(idatencion))
        atencion.delete()
        return JsonResponse({"existe":0}, status = 200)



# Create your views here.
