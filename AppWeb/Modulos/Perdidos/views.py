from django.shortcuts import render, redirect
from django.views.generic import CreateView, View
from .models import Perdido
from django.db.models import Q
from AppWeb.Modulos.Adopciones.models import Can
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from AppWeb.Inicio.mixins import *
from AppWeb.Modulos.Usuarios.models import HistorialUsuarios


class AdminListarPerdidos(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        perdidos = Perdido.objects.all()
        canes = Can.objects.all()
        search = self.request.GET.get('search')
        if search:
            perdidos = Perdido.objects.filter(
                Q(can_perdido__nombre__icontains=search) |
                Q(can_perdido__id_raza__nombre__icontains=search) |
                Q(can_perdido__sexo__icontains=search)
            )
        return render(self.request, 'Administrador/Perdidos/Perdidos.html', {'perdidos': perdidos, 'canes': canes})


class AdminRegistrarPerdido(SuperUsuarioMixin, View):
    def post(self, *args, **kwargs):
        try:
            usuario = self.request.user
            fecha = self.request.POST['txtFecha']
            comentario = self.request.POST['txtComentario']
            can = self.request.POST['txtCan']
            id_can = Can.objects.get(nombre=can)
            Perdido.objects.create(fecha=fecha, comentario=comentario, can_perdido=id_can)
            id_can.estado = False
            id_can.save()
            historial = HistorialUsuarios.objects.create(
                tipo="Asigno al can " + id_can.nombre + " como perdido", usuario=usuario)
            messages.success(self.request, 'Se registro al perdido')
        except ObjectDoesNotExist:
            messages.error(self.request, 'Hubo algún error')
        except IntegrityError:
            messages.error(self.request, 'El can ya se encuentra como perdido')
        return redirect('vista_listar_perdidos')


class AdminEncontrado(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        usuario = self.request.user
        perdido = Perdido.objects.get(can_perdido=pk)
        can = Can.objects.get(id=pk)
        if can.caso_independiente:
            historial = HistorialUsuarios.objects.create(
                tipo="Asigno al can" + can.nombre + " como encontrado y se borro", usuario=usuario)
            can.delete()
            messages.success(self.request, 'Can de caso independiente encontrado')
        else:
            perdido.delete()
            can.estado = True
            can.save()
            historial = HistorialUsuarios.objects.create(
                tipo="Asigno al can" + can.nombre + " como encontrado", usuario=usuario)
            messages.success(self.request, 'Can registrado como encontrado')
        return redirect('vista_listar_perdidos')
