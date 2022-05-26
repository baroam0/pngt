
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from .forms import EscuelaForm
from .models import Escuela


def listadoescuelas(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get("txtBuscar")
        if parametro == "":    
            consulta = Escuela.objects.all().order_by('descripcion')
        else:
            consulta = Escuela.objects.filter(
                descripcion__icontains=parametro).order_by('descripcion')
    else:
        consulta = Escuela.objects.all().order_by('pk')

    paginador = Paginator(consulta, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1

    resultados = paginador.get_page(page)
    return render(request, 'escuelas/escuela_list.html', {'resultados': resultados})


def nuevaescuela(request):
    if request.POST:
        form = EscuelaForm(request.POST)
                
        if form.is_valid():
            form.save()
            consulta = Escuela.objects.latest('pk')
            if consulta.operativo == True:
                escuelas = Escuela.objects.all().exclude(pk=consulta.pk)
                for esc in escuelas:
                    esc.operativo = False
                    esc.save()

            messages.success(
                request,
                "SE HAN GUARDADO DE LA ESCUELA ")
                #return redirect('/pacienteeditar/' + str(consulta.pk))
            return redirect('/escuelalistado')
        else:
            return render(
                request,
                'escuelas/escuelas_edit.html',
                {
                    "form": form,
                })
    else:
        form = EscuelaForm()
        return render(
            request,
            'escuelas/escuela_edit.html',
            {
                "form": form,
            }
        )


def editarescuela(request, pk):
    consulta = Escuela.objects.get(pk=pk)
    
    if request.POST:
        form = EscuelaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            if consulta.operativo == True:
                escuelas = Escuela.objects.all().exclude(pk=consulta.pk)
                for esc in escuelas:
                    esc.operativo = False
                    esc.save()
            messages.success(request, "SE HA MOFICICADO LA ESCUELA")
            return redirect('/escuelalistado')
        else:
            return render(request, "escuelas/escuela_edit.html", {"form": form})
    else:
        form = EscuelaForm(instance=consulta)

        return render(
            request,
            'escuelas/escuela_edit.html',
            {
                "form": form,
            }
        )

# Create your views here.
