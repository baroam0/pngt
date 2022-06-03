
from django.contrib import messages
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from django.shortcuts import render, redirect

from .forms import MedicamentoForm, RecetaForm, RecetaDetalleForm, EntregaMedicamentoForm
from .models import Medicamento, Receta, RecetaDetalle, EntregaMedicamento
from pacientes.models import Paciente


def listadomedicamentos(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get("txtBuscar")
        if parametro == "":    
            consulta = Medicamento.objects.all().order_by('descripcion')
        else:
            consulta = Medicamento.objects.filter(
                descripcion__icontains=parametro).order_by('descripcion')
    else:
        parametro=''
        consulta = Medicamento.objects.all().order_by('pk')

    paginador = Paginator(consulta, 10)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1

    resultados = paginador.get_page(page)
    return render(
        request,
        'medicamentos/medicamento_list.html',
        {
            'resultados': resultados,
            'parametro':parametro
        }
    )


def nuevomedicamento(request):
    if request.POST:
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "SE HAN GUARDADO EL MEDICAMENTO ")
                #return redirect('/pacienteeditar/' + str(consulta.pk))
            return redirect('/medicamentolistado')
        else:
            return render(
                request,
                'medicamentos/medicamento_edit.html',
                {
                    "form": form,
                })
    else:
        form = MedicamentoForm()
        return render(
            request,
            'medicamentos/medicamento_edit.html',
            {
                "form": form,
            }
        )


def editarmedicamento(request, pk):
    consulta = Medicamento.objects.get(pk=pk)

    if request.POST:
        form = MedicamentoForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, "SE HA MOFICICADO EL MEDICAMENTO")
            return redirect('/medicamentolistado')
        else:
            return render(request, "medicamentos/medicamento_edit.html", {"form": form})
    else:
        form = MedicamentoForm(instance=consulta)

        return render(
            request,
            'medicamentos/medicamento_edit.html',
            {
                "form": form,
            }
        )


def nuevareceta(request, pk):
    paciente = Paciente.objects.filter(pk=pk)

    if request.POST:
        recetaform = RecetaForm(request.POST)
        recetadetalleform = RecetaDetalleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "SE HAN GUARDADO LOS DATOS DE LA ATENCION")
                #return redirect('/pacienteeditar/' + str(consulta.pk))
            return redirect('/atencioneslistado/')
        else:
            return render(
                request,
                'atenciones/atencion_link.html',
                {
                    "form": form,
                    "paciente": paciente
                })
    else:
        recetaform = RecetaForm()
        recetadetalleform = RecetaDetalleForm()

        return render(
            request,
            'medicamentos/receta_edit.html',
            {
                "recetaform": recetaform,
                "recetadetalleform": recetadetalleform,
                "paciente": paciente
            }
        )


def listadoentregamedicamento(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get("txtBuscar")
        if parametro == "":
            consulta = EntregaMedicamento.objects.all().order_by('pk')
        else:
            consulta = EntregaMedicamento.objects.filter(
                medicamento__descripcion__icontains=parametro).order_by("pk")
    else:
        parametro=''
        consulta = EntregaMedicamento.objects.all().order_by('pk')

    paginador = Paginator(consulta, 10)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1

    resultados = paginador.get_page(page)
    return render(
        request,
        'medicamentos/entregamedicamento_list.html',
        {
            'resultados': resultados,
            'parametro':parametro
        }
    )


def nuevoentregamedicamento(request):
    if request.POST:
        form = EntregaMedicamentoForm(request.POST)
        if form.is_valid():
            form.save()
            ultimaentrega = EntregaMedicamento.objects.latest('pk')
            medicamento = Medicamento.objects.get(pk=ultimaentrega.medicamento.pk)
            medicamento.cantidad = int(medicamento.cantidad) - int(ultimaentrega.cantidad)
            medicamento.save()
            messages.success(
                request,
                "SE HAN GUARDADO EL MEDICAMENTO ")
            return redirect('/entregamedicamentolistado')
        else:
            return render(
                request,
                'medicamentos/entregamedicamento_edit.html',
                {
                    "form": form,
                })
    else:
        form = EntregaMedicamentoForm()
        return render(
            request,
            'medicamentos/entregamedicamento_edit.html',
            {
                "form": form,
            }
        )


def editarentregamedicamento(request, pk):
    consulta = EntregaMedicamento.objects.get(pk=pk)
    cantidadanterior = consulta.cantidad

    if request.POST:
        form = EntregaMedicamentoForm(request.POST, instance=consulta)
        if form.is_valid():
            entregacantidad = request.POST['cantidad']
            medicamento = Medicamento.objects.get(pk=consulta.medicamento.pk)
            medicamento.cantidad = int(medicamento.cantidad) + int(cantidadanterior) - int(entregacantidad)
            medicamento.save()
            form.save()
            messages.success(request, "SE HA MOFICICADO EL MEDICAMENTO")
            return redirect('/entregamedicamentolistado')
        else:
            return render(request, "medicamentos/entregamedicamento_edit.html", {"form": form})
    else:
        form = EntregaMedicamentoForm(instance=consulta)
        return render(
            request,
            'medicamentos/entregamedicamento_edit.html',
            {
                "form": form,
            }
        )

# Create your views here.
