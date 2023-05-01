import json
from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, UpdateView
import requests
from AppWeb.Inicio.mixins import *
from AppWeb.Modulos.Adopciones.models import Can
from AppWeb.Modulos.Usuarios.models import User
from .models import Donador
from .forms import *
from AppWeb.Modulos.Usuarios.models import HistorialUsuarios


class VistaDonaciones(SuperUsuarioMixin, TemplateView):
    template_name = 'Administrador/Donaciones/registrar_donacion.html'


class SolicitarPadrinaje(View):
    def get(self, *args, **kwargs):
        id_can = self.kwargs['pk']
        can = Can.objects.get(id=id_can)
        fecha_nacimiento = can.fecha_nacimiento
        edad = relativedelta(datetime.now(), fecha_nacimiento)
        return render(self.request, 'pages/vista_canes/padrinaje.html', {'can': can, 'edad': edad})


class VistaDonar(View):
    def post(self, *args, **kwargs):
        url = 'https://botonpagoapiv1.azurewebsites.net/api/v1/main/getPaymentButton'
        foto = self.request.POST['txtFoto']
        datos = {
            "photo": "yJ2ZNYNk/kai3YCXD4hoNg==", "title": "Camisas",
            "detail": "Camisas Ejecutivas, Talla M , Colores Rojo y Blanco",
            "currency": "BOB",
            "amount": 123
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        r = requests.post(url, headers=headers, data=json.dumps(datos))
        print(r.json())
        return redirect('vista_donaciones')


class Donaciones(View):
    def get(self, *args, **kwargs):
        padrinos = User.objects.filter(is_padrino=True)
        return render(self.request, 'Administrador/Donaciones/donaciones.html', {'padrinos': padrinos})


class RegistrarDonacion(View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        padrino = User.objects.get(id=pk)
        canes = Can.objects.filter(adoptado=False)
        return render(self.request, 'Administrador/Donaciones/registrar_donacion.html',
                      {'padrino': padrino, 'canes': canes})

    def post(self, *args, **kwargs):
        pk = self.kwargs['pk']
        usuario = self.request.user
        padrino = User.objects.get(id=pk)
        fecha = self.request.POST['txtFecha']
        monto = self.request.POST['txtMonto']
        id_can = self.request.POST['txtCan']
        can = Can.objects.get(nombre=id_can)
        donacion = Donador.objects.create(fecha=fecha, monto=monto, id_can_id=can.id, usuario_donador=padrino)
        historial = HistorialUsuarios.objects.create(
            tipo="Registro una nueva donación " + donacion.monto + " " + donacion.usuario_donador.apellidos,
            usuario=usuario)
        messages.success(self.request, 'Donación registrada correctamente')
        return redirect('vista_donaciones')


class HistorialDonaciones(View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        padrino = User.objects.get(id=pk)
        canes = Donador.objects.filter(usuario_donador=pk)
        return render(self.request, 'Administrador/Donaciones/historial_donacion.html',
                      {'padrino': padrino, 'canes': canes})


class EditarDonacion(UpdateView):
    model = Donador
    template_name = 'Administrador/Donaciones/editar_donacion.html'
    form_class = FormEditarDonacion

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['canes'] = Can.objects.filter(adoptado=False)
        return context

    def form_valid(self, form):
        form.save()
        pk = self.kwargs['pk']
        usuario = self.request.user
        id_can = self.request.POST['txtCan']
        can = Can.objects.get(nombre=id_can)
        fecha = self.request.POST['txtFecha']
        donador = Donador.objects.get(id=pk)
        donador.fecha = fecha
        donador.id_can_id = can.id
        donador.save()
        historial = HistorialUsuarios.objects.create(
            tipo="Actualizo los datos de la donación " + donador.monto + " " + donador.usuario_donador.apellidos,
            usuario=usuario)
        messages.success(self.request, 'Donación editada correctamente')
        return redirect('vista_historial_donacion', donador.usuario_donador_id)


class EliminarDonacion(View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        usuario = self.request.user
        donacion = Donador.objects.get(id=pk)
        padrino = donacion.usuario_donador_id
        historial = HistorialUsuarios.objects.create(
            tipo="Elimino los datos de la donación " + donacion.monto + " " + donacion.usuario_donador.apellidos,
            usuario=usuario)
        donacion.delete()
        messages.success(self.request, 'Donación eliminada correctamente')
        return redirect('vista_historial_donacion', padrino)
