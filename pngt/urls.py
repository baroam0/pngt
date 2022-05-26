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

from escuelas.views import listadoescuelas, nuevaescuela, editarescuela
from pacientes.views import listadopaciente, nuevopaciente, editarpaciente
from atenciones.views import (listadoatenciones, nuevaatencion,
    listadoespecialidades, nuevaespecialidad, editarespecialidad,
    ajaxgraficoatencionporescuela, atencionporescuela)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('atencionporescuela/', atencionporescuela),
    path('ajaxatencionescuela/', ajaxgraficoatencionporescuela),
    path('atencioneslistado/', listadoatenciones),
    path('atencionnueva/', nuevaatencion),
    path('practicaslistado/', listadoespecialidades),
    path('practicanueva/', nuevaespecialidad),
    path('practicaeditar/<int:pk>', editarespecialidad),
    path('escuelalistado/', listadoescuelas),
    path('escuelanueva/', nuevaescuela),
    path('escuelaeditar/<int:pk>', editarescuela),
    path('pacientelistado/', listadopaciente),
    path('pacientenuevo/', nuevopaciente),
    path('pacienteeditar/<int:pk>', editarpaciente),
]
