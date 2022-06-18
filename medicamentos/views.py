
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from django.shortcuts import render, redirect

from .forms import (MedicamentoForm, RecetaForm, RecetaDetalleForm,
                    EntregaMedicamentoForm, PresentacionMedicaForm,
                    RecepcionMedicamentoForm)

from .models import (Medicamento, Receta, RecetaDetalle, 
                     EntregaMedicamento, PresentacionMedica, RecepcionaMedicamento)

from escuelas.models import Escuela
from pacientes.models import Paciente


def listadomedicamentos(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get("txtBuscar")
        if parametro == "":    
            consulta = Medicamento.objects.all().order_by('descripcion')
        else:
            consulta = Medicamento.objects.filter(
                Q(descripcion__icontains=parametro) |
                Q(presentacion__descripcion__icontains=parametro)).order_by('descripcion')
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


def impresionlistadomedicamento(request):
    escuela = Escuela.objects.get(operativo=True)
    parametro = request.GET.get("txtBuscar")
    resultados = Medicamento.objects.filter(
                descripcion__icontains=parametro).order_by('descripcion')
    return render(
        request,
        "medicamentos/reporte_listado.html",
        {
            "escuela": escuela,
            "resultados": resultados
        }
    )


def listadopresentacionmedica(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get("txtBuscar")
        if parametro == "":
            consulta = PresentacionMedica.objects.all().order_by('descripcion')
        else:
            consulta = PresentacionMedica.objects.filter(
                descripcion__icontains=parametro).order_by('descripcion')
    else:
        parametro=''
        consulta = PresentacionMedica.objects.all().order_by('descripcion')

    paginador = Paginator(consulta, 10)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1

    resultados = paginador.get_page(page)
    return render(
        request,
        'medicamentos/presentacionmedicamento_list.html',
        {
            'resultados': resultados,
            'parametro':parametro
        }
    )


def nuevapresentacionmedica(request):
    if request.POST:
        form = PresentacionMedicaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "SE HAN GUARDADO LA PRESENTACION DEL MEDICAMENTO")
                #return redirect('/pacienteeditar/' + str(consulta.pk))
            return redirect('/medicamentolistado')
        else:
            return render(
                request,
                'medicamentos/presentacionmedicamento_edit.html',
                {
                    "form": form,
                })
    else:
        form = PresentacionMedicaForm()
        return render(
            request,
            'medicamentos/presentacionmedicamento_edit.html',
            {
                "form": form,
            }
        )


def editarpresentacionmedica(request, pk):
    consulta = PresentacionMedica.objects.get(pk=pk)

    if request.POST:
        form = PresentacionMedicaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, "SE HA MOFICICADO LA PRESENTACION")
            return redirect('/presentacionmedicalistado')
        else:
            return render(request, "medicamentos/medicamento_edit.html", {"form": form})
    else:
        form = PresentacionMedicaForm(instance=consulta)

        return render(
            request,
            'medicamentos/presentacionmedicamento_edit.html',
            {
                "form": form,
            }
        )


def listadorecepcionmedicamento(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get("txtBuscar")
        if parametro == "":
            consulta = RecepcionaMedicamento.objects.all().order_by('pk')
        else:
            consulta = RecepcionaMedicamento.objects.filter(
                medicamento__descripcion__icontains=parametro).order_by("pk")
    else:
        parametro=''
        consulta = RecepcionaMedicamento.objects.all().order_by('pk')

    paginador = Paginator(consulta, 10)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1

    resultados = paginador.get_page(page)
    return render(
        request,
        'medicamentos/recepcionmedicamento_list.html',
        {
            'resultados': resultados,
            'parametro':parametro
        }
    )


def nuevarecepcionmedicamento(request):
    if request.POST:
        form = RecepcionMedicamentoForm(request.POST)
        if form.is_valid():
            form.save()
            ultimarecepcion = RecepcionaMedicamento.objects.latest('pk')
            medicamento = Medicamento.objects.get(pk=ultimarecepcion.medicamento.pk)
            medicamento.cantidad = int(medicamento.cantidad) + int(ultimarecepcion.cantidad)
            medicamento.save()
            messages.success(
                request,
                "SE HAN GUARDADO LA RECEPCION ")
            return redirect('/recepcionmedicamentolistado')
        else:
            return render(
                request,
                'medicamentos/recepcionmedicamento_edit.html',
                {
                    "form": form,
                })
    else:
        form = RecepcionMedicamentoForm()
        return render(
            request,
            'medicamentos/recepcionmedicamento_edit.html',
            {
                "form": form,
            }
        )


def editarrecepcionmedicamento(request, pk):
    consulta = RecepcionaMedicamento.objects.get(pk=pk)
    cantidadanterior = consulta.cantidad

    if request.POST:
        form = RecepcionMedicamentoForm(request.POST, instance=consulta)
        if form.is_valid():
            recepcioncantidad = request.POST['cantidad']
            medicamento = Medicamento.objects.get(pk=consulta.medicamento.pk)
            medicamento.cantidad = int(medicamento.cantidad) - int(cantidadanterior) + int(recepcioncantidad)
            medicamento.save()
            form.save()
            messages.success(request, "SE HA MOFICICADO EL MEDICAMENTO")
            return redirect('/recepcionmedicamentolistado')
        else:
            return render(request, "medicamentos/recepcionmedicamento_edit.html", {"form": form})
    else:
        form = EntregaMedicamentoForm(instance=consulta)
        return render(
            request,
            'medicamentos/recepcionmedicamento_edit.html',
            {
                "form": form,
            }
        )

# Create your views here.
