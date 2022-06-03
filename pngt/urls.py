"""pngt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from .views import home
from escuelas.views import listadoescuelas, nuevaescuela, editarescuela
from medicamentos.views import (
    listadomedicamentos, nuevomedicamento, editarmedicamento, nuevareceta,
    listadoentregamedicamento, nuevoentregamedicamento, editarentregamedicamento)

from pacientes.views import listadopaciente, nuevopaciente, editarpaciente, ajaxpaciente, nuevopacientepreload

from atenciones.views import (
    listadoatenciones, nuevaatencion,editaratencion, listadoespecialidades, 
    nuevaespecialidad, editarespecialidad, ajaxgraficoatencionporescuela, 
    atencionporescuela, nuevaatencionlink, renderticket
    )

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('ajaxpaciente/', ajaxpaciente),
    path('atencionporescuela/', atencionporescuela),
    path('ajaxatencionescuela/', ajaxgraficoatencionporescuela),
    path('atencioneslistado/', listadoatenciones),
    path('atencionnueva/', nuevaatencion),
    path('atencionlink/<int:pk>', nuevaatencionlink),
    path('atencioneditar/<int:pk>', editaratencion),
    path('practicaslistado/', listadoespecialidades),
    path('practicanueva/', nuevaespecialidad),
    path('practicaeditar/<int:pk>', editarespecialidad),
    path('escuelalistado/', listadoescuelas),
    path('escuelanueva/', nuevaescuela),
    path('escuelaeditar/<int:pk>', editarescuela),
    path('entregamedicamentolistado/', listadoentregamedicamento),
    path('entregamedicamentonuevo/', nuevoentregamedicamento),
    path('entregamedicamentoeditar/<int:pk>', editarentregamedicamento),
    path('medicamentolistado/', listadomedicamentos),
    path('medicamentonuevo/', nuevomedicamento),
    path('medicamentoeditar/<int:pk>', editarmedicamento),
    path('recetanueva/<int:pk>', nuevareceta),
    path('pacientelistado/', listadopaciente),
    path('pacientenuevo/', nuevopaciente),
    path('pacientenuevopreload/<str:rawdata>', nuevopacientepreload),
    path('pacienteeditar/<int:pk>', editarpaciente),
    path('renderticket/<int:pk>', renderticket)
]
