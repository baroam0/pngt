
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, QuerySet
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q

from escuelas.models import Escuela

from .forms import AtencionForm, EspecialidadForm
from .models import Atencion, Especialidad


def listadoatenciones(request):
    escueladefault = Escuela.objects.get(operativo=True)
    if "txtBuscar" in request.GET:
        parametro = request.GET.get("txtBuscar")
        if parametro == "":
            #consulta = Atencion.objects.all().order_by('pk')
            consulta = Atencion.objects.filter(escuela=escueladefault.pk)
        else:
            if parametro.isnumeric():
                idatencion = int(parametro)
            consulta = Atencion.objects.filter(
                Q(pk=idatencion) |
                Q(paciente__apellido__icontains=parametro) |
                Q(paciente__nombre__contains=parametro) |
                Q(paciente__numerodocumento__contains=parametro) &
                Q(escuela=escueladefault.pk)
            ).order_by('pk')
    else:
        consulta = Atencion.objects.all().order_by('pk')

    paginador = Paginator(consulta, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1

    resultados = paginador.get_page(page)
    return render(request, 'atenciones/atencion_list.html', {'resultados': resultados})


def nuevaatencion(request):
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
                'atenciones/atencion_nuevo.html',
                {
                    "form": form,
                })
    else:
        form = AtencionForm()
        return render(
            request,
            'atenciones/atencion_nuevo.html',
            {
                "form": form,
            }
        )


def editaratencion(request, pk):
    consulta = Atencion.objects.get(pk=pk)
    
    if request.POST:
        form = AtencionForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, "SE HA MOFICICADO EL PACIENTE")
            return redirect('/pacientelistado')
        else:
            return render(request, "atenciones/atencion_nuevo.html", {"form": form})
    else:
        form = AtencionForm(instance=consulta)

        return render(
            request,
            'atenciones/atencion_nuevo.html',
            {
                "form": form,
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
            messages.success(
                request,
                "SE HAN GUARDADO LOS DATOS DE LA PRACTICA")
                #return redirect('/pacienteeditar/' + str(consulta.pk))
            return redirect('/practicaslistado', str(consulta.pk))
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
            messages.success(request, "SE HA MOFICICADO LA PRACTICA")
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
        results = (Atencion.objects.filter(escuela=escuela.pk).values('especialidad').annotate(dcount=Count('especialidad')).order_by())

    
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



# Create your views here.
