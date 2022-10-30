from django.shortcuts import render, redirect
from django.views.generic import CreateView, View
from .models import Perdido
from django.db.models import Q
from AppWeb.Modulos.Adopciones.models import Can
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


class AdminListarPerdidos(View):
    def get(self, *args, **kwargs):
        perdidos = Perdido.objects.all()
        canes = Can.objects.all()
        search = self.request.GET.get('search')
        if search:
            perdidos = Perdido.objects.filter(
                Q(can_perdido__nombre=search) |
                Q(can_perdido__id_raza__nombre=search) |
                Q(can_perdido__sexo=search)
            )
        return render(self.request, 'Administrador/Perdidos/Perdidos.html', {'perdidos': perdidos, 'canes': canes})


class AdminRegistrarPerdido(View):
    def post(self, *args, **kwargs):
        try:
            fecha = self.request.POST['txtFecha']
            comentario = self.request.POST['txtComentario']
            can = self.request.POST['txtCan']
            id_can = Can.objects.get(nombre=can)
            Perdido.objects.create(fecha=fecha, comentario=comentario, can_perdido=id_can)
            id_can.estado = False
            id_can.save()
            messages.success(self.request, 'Se registro al perdido')
        except ObjectDoesNotExist:
            messages.error(self.request, 'Hubo algún error')
        except IntegrityError:
            messages.error(self.request, 'El can ya se encuentra como perdido')
        return redirect('vista_listar_perdidos')


class AdminEncontrado(View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        perdido = Perdido.objects.get(can_perdido=pk)
        can = Can.objects.get(id=pk)
        if can.caso_independiente:
            can.delete()
            messages.success(self.request, 'Can de caso independiente encontrado')
        else:
            perdido.delete()
            can.estado = True
            can.save()
            messages.success(self.request, 'Can registrado como encontrado')
        return redirect('vista_listar_perdidos')
