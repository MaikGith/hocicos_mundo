from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView, TemplateView
from django.contrib import messages
from .models import *
from .forms import *
from django.utils.datastructures import MultiValueDictKeyError
from django.db import IntegrityError
from datetime import datetime
from dateutil.relativedelta import relativedelta
# pdf
from django.template.loader import *
from weasyprint import HTML, CSS
from django.conf import settings
import os.path
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy


class AdminListarCan(View):
    def get(self, *args, **kwargs):
        search = self.request.GET.get('search')
        canes = Can.objects.all()
        razas = Raza.objects.all()
        if search:
            canes = Can.objects.filter(
                Q(nombre__icontains=search) |
                Q(id_raza__nombre=search) |
                Q(sexo__icontains=search)
            )
        return render(self.request, 'Administrador/Can/Canes.html', {'canes': canes, 'razas': razas})


class AdminRegistroCan(View):
    def post(self, *args, **kwargs):
        try:
            nombre = self.request.POST['nombre_can']
            sexo = self.request.POST['sexo_can']
            fecha = self.request.POST['fecha_can']
            color = self.request.POST['color_can']
            personalidad = self.request.POST['personalidad_can']
            altura = self.request.POST['tamano_can']
            foto = self.request.FILES['foto_can']
            raza_nombre = self.request.POST['raza_can']
            raza_id = Raza.objects.get(nombre=raza_nombre).id
            nuevo_can = Can.objects.create(nombre=nombre, sexo=sexo, fecha_nacimiento=fecha, color=color,
                                           personalidad=personalidad, altura=altura, foto=foto, id_raza_id=raza_id)
            nuevo_can.save()
            messages.success(self.request, 'Can registrado')
        except ObjectDoesNotExist:
            messages.error(self.request, 'Hubo algún error')
        except IntegrityError:
            messages.error(self.request, 'El can ya se encuentra registrado')
        return redirect('vista_listar_can')


class AdminEditarCan(UpdateView):
    model = Can
    template_name = 'Administrador/Can/Editar/canes.html'
    form_class = FormCanEditar

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, *args, **kwargs):
        pk = self.kwargs['pk']
        form = self.get_form()
        form.save()
        id_raza = self.request.POST['raza_can']
        fecha = self.request.POST['txtFecha']
        raza = Raza.objects.get(nombre=id_raza).id
        can = Can.objects.get(id=pk)
        can.id_raza_id = raza
        can.fecha_nacimiento = fecha
        try:
            foto = self.request.FILES['txtFoto']
            can.foto = foto
        except MultiValueDictKeyError:
            messages.error(self.request, "Error")
        can.save()
        messages.success(self.request, "Can editado")
        return redirect('vista_listar_can')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        razas = Raza.objects.all()
        context['razas'] = razas
        return context


class AdminEliminarCan(View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        can = Can.objects.get(id=pk)
        can.delete()
        messages.info(self.request, "Can eliminado")
        return redirect('vista_listar_can')


class AdminRegistrarEsterilizacion(View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        can = Can.objects.get(id=pk)
        return render(self.request, 'Administrador/Can/Esterilizacion.html', {'can': can})

    def post(self, *args, **kwargs):
        pk = self.kwargs['pk']
        can = Can.objects.get(id=pk)
        n_tattoo = self.request.POST['txtTattoo']
        fecha = self.request.POST['txtFecha']
        Esterilizacion.objects.create(n_tattoo=n_tattoo, fecha=fecha, cam_id=pk)
        can.esterilizado = True
        can.save()
        messages.success(self.request, 'Registro de esterilización')
        return redirect('vista_listar_can')


class AdminEditarEsterilizacion(View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        esterilizacion = Esterilizacion.objects.get(cam_id=pk)
        return render(self.request, 'Administrador/Can/Editar/esterilizacion.html', {'esterilizacion': esterilizacion})

    def post(self, *args, **kwargs):
        pk = self.kwargs['pk']
        n_tattoo = self.request.POST['txtTattoo']
        fecha = self.request.POST['txtFecha']
        esterilizacion = Esterilizacion.objects.get(id=pk)
        esterilizacion.n_tattoo = n_tattoo
        esterilizacion.fecha = fecha
        esterilizacion.save()
        messages.success(self.request, 'Esterilización editada')
        return redirect('vista_listar_can')


class AdminListarRaza(View):
    def get(self, *args, **kwargs):
        razas = Raza.objects.all()
        return render(self.request, 'Administrador/Can/Razas.html', {'razas': razas})


class AdminRegistroRaza(View):
    def post(self, request):
        nombre = request.POST['race_can']
        race = Raza.objects.create(nombre=nombre)
        return redirect('vista_listar_raza')


class AdminEditarRaza(UpdateView):
    model = Raza
    template_name = 'Administrador/Can/Editar/raza.html'
    form_class = FormRazaEditar

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, *args, **kwargs):
        form = self.get_form()
        form.save()
        messages.success(self.request, "Raza editado")
        return redirect('vista_listar_raza')


class AdminEliminarRaza(View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        raza = Raza.objects.get(id=pk)
        raza.delete()
        messages.info(self.request, "Raza eliminado")
        return redirect('vista_listar_raza')


class AdminListarVacuna(View):
    def get(self, request):
        search = self.request.GET.get('search')
        canes = Can.objects.all()
        if search:
            canes = Can.objects.filter(
                Q(nombre__icontains=search) |
                Q(id_raza__nombre=search) |
                Q(sexo__icontains=search)
            )
        return render(request, 'Administrador/Can/Vacunas.html', {'canes': canes})


class AdminRegistrarVacuna(View):
    def post(self, *args, **kwargs):
        nombre = self.request.POST['txtNombre']
        caracteristicas = self.request.POST['txtCaracteristicas']
        Vacuna.objects.create(nombre=nombre, caracteristicas=caracteristicas)
        messages.success(self.request, 'Vacuna registrada')
        return redirect('vista_listar_vacuna')


class AdminAsignarVacuna(View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        can = Can.objects.get(id=pk)
        vacunas = Vacuna.objects.all()
        return render(self.request, 'Administrador/Can/Registrar/vacunas_canes.html',
                      {'vacunas': vacunas, 'can': can})

    def post(self, *args, **kwargs):
        pk = self.kwargs['pk']
        fecha = self.request.POST['txtFecha']
        vacuna = self.request.POST['txtVacuna']
        Vacunas_Can.objects.create(fecha=fecha, can_id=pk, vacuna_id=vacuna)
        messages.success(self.request, 'Vacuna asignada')
        return redirect('vista_listar_vacuna')


class AdminHistorialVacuna(View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        can = Can.objects.get(id=pk)
        historiales = Vacunas_Can.objects.filter(can_id=pk).distinct()
        return render(self.request, 'Administrador/Can/Historial_vacunas.html',
                      {'historiales': historiales, 'can': can})


class AdminEliminarVacuna(View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        vacuna = Vacunas_Can.objects.get(id=pk)
        id_can = vacuna.can_id
        vacuna.delete()
        messages.info(self.request, "Vacuna eliminado")
        return redirect('vista_historial_vacuna', id_can)


class AdminEditarVacunaCan(View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        vacuna_asignada = Vacunas_Can.objects.get(id=pk)
        vacunas = Vacuna.objects.all()
        return render(self.request, 'Administrador/Can/Editar/vacuna.html',
                      {'vacuna_asignada': vacuna_asignada, 'vacunas': vacunas})

    def post(self, *args, **kwargs):
        pk = self.kwargs['pk']
        fecha = self.request.POST['txtFecha']
        vacuna = self.request.POST['txtVacuna']
        vacuna_can = Vacunas_Can.objects.get(id=pk)
        vacuna_can.fecha = fecha
        vacuna_can.vacuna_id = vacuna
        vacuna_can.save()
        id_can = vacuna_can.can_id
        messages.success(self.request, 'Vacuna editada')
        return redirect('vista_historial_vacuna', id_can)


class AdminListarAdopciones(View):
    def get(self, *args, **kwargs):
        adoptadores = Usuario_Adoptivo.objects.all()
        return render(self.request, 'Administrador/Adopciones/adopciones.html', {'adoptadores': adoptadores})


class AdminRegistraAdopcion(View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        canes = Can.objects.filter(adoptado=False)
        adoptador = Usuario_Adoptivo.objects.get(id=pk)
        return render(self.request, 'Administrador/Adopciones/Registrar/adopcion.html',
                      {'canes': canes, 'adoptador': adoptador})

    def post(self, *args, **kwargs):
        try:
            pk = self.kwargs['pk']
            can = self.request.POST['txtCan']
            usuario_adoptivo = Usuario_Adoptivo.objects.get(id=pk)
            if usuario_adoptivo.cantidad_max < 2:
                can = Can.objects.get(nombre=can)
                can.adoptado = True
                now = datetime.now()
                can.fecha_adopcion = now.date()
                can.id_usuario_adoptivo_id = usuario_adoptivo.id
                can.save()
                usuario_adoptivo.cantidad_max = usuario_adoptivo.cantidad_max + 1
                usuario_adoptivo.save()
                messages.success(self.request, 'Adopción registrada')
            else:
                messages.info(self.request, 'La operación no se ejecuto')
        except ObjectDoesNotExist:
            messages.error(self.request, 'Hubo algún error')
        return redirect('vista_listar_adopciones')


class AdminListarACargo(View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        adoptador = Usuario_Adoptivo.objects.get(id=pk)
        canes = Can.objects.filter(id_usuario_adoptivo=pk)
        return render(self.request, 'Administrador/Adopciones/a_cargo.html', {'adoptador': adoptador, 'canes': canes})


class AdminImprimirAdopcion(View):
    def get(self, *args, **kwargs):
        try:
            pk = self.kwargs['pk']
            can = Can.objects.get(id=pk)
            edad = relativedelta(datetime.now(), can.fecha_nacimiento).years
            esterilizacion = {'n_tattoo': 'No realizado'}
            if can.esterilizado:
                esterilizacion = Esterilizacion.objects.get(cam_id=can.id)
            vacunas = Vacunas_Can.objects.filter(can_id=pk)
            usuario_adoptivo = Usuario_Adoptivo.objects.get(id=can.id_usuario_adoptivo_id).usuario_id
            usuario = User.objects.get(id=usuario_adoptivo)
            context = {'can': can, 'edad': edad, 'vacunas': vacunas, 'usuario': usuario,
                       'esterilizacion': esterilizacion}
            template = get_template('Administrador/pdf/formulario_adopcion.html')
            html = template.render(context)
            css_url = os.path.join(settings.BASE_DIR, 'static/static-pdf/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=self.request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('vista_listar_adopciones'))


class AdminEliminarAdopcion(View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        can = Can.objects.get(id=pk)
        id_usuario = can.id_usuario_adoptivo_id
        can.adoptado = False
        can.id_usuario_adoptivo_id = None
        can.save()
        usuario = Usuario_Adoptivo.objects.get(id=id_usuario)
        usuario.cantidad_max = usuario.cantidad_max - 1
        usuario.save()
        return redirect('vista_listar_a_cargo', id_usuario)


class AdminListarReuniones(View):
    def get(self, *args, **kwargs):
        adoptadores = Usuario_Adoptivo.objects.all()
        return render(self.request, 'Administrador/Reuniones/reuniones.html', {'adoptadores': adoptadores})


class AdminRegistrarReuniones(View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        adoptante = Usuario_Adoptivo.objects.get(id=pk)
        return render(self.request, 'Administrador/Reuniones/Registrar/reunion.html', {'adoptante': adoptante})

    def post(self, *args, **kwargs):
        try:
            pk = self.kwargs['pk']
            fecha = self.request.POST['txtFecha']
            motivo = self.request.POST['txtMotivo']
            Reunion.objects.create(fecha=fecha, motivo=motivo, usuario_adoptivo=pk)
        except ObjectDoesNotExist:
            messages.error(self.request, 'Hubo algún error')
        return redirect('vista_listar_reuniones')
