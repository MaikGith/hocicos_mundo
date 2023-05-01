from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView, TemplateView
from django.contrib import messages
from .models import *
from .forms import *
from django.utils.datastructures import MultiValueDictKeyError
from django.db import IntegrityError
# pdf
from django.template.loader import *
from weasyprint import HTML, CSS
from django.conf import settings
import os.path
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from AppWeb.Inicio.mixins import *
from AppWeb.Modulos.Usuarios.models import HistorialUsuarios
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os
from pydrive2.files import FileNotUploadedError
from datetime import datetime
from dateutil.relativedelta import relativedelta

directorio_credenciales = 'AppWeb/Modulos/Adopciones/credentials_module.json'


def login():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)

    if gauth.access_token_expired:
        gauth.Refresh()
        gauth.SaveCredentialsFile(directorio_credenciales)
    else:
        gauth.Authorize()

    return GoogleDrive(gauth)


def SubirArchivo(nombre, ruta):
    credenciales = login()
    archivo = credenciales.CreateFile(
        {'parents': [{"kind": "drive#fileLink", "id": '1Dq9pG1LtCsvuN2oY4SbRk77qpqBozK6i'}]})
    archivo['title'] = nombre
    archivo.SetContentFile(ruta)
    archivo.Upload()
    query = "title = " + "'" + nombre + "'"
    lista_archivos = credenciales.ListFile({'q': query}).GetList()
    dato = lista_archivos.pop(0)['id']
    print(dato)
    return dato


class AdminListarCan(SuperUsuarioMixin, View):
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


# class AdminRegistroCan(SuperUsuarioMixin, View):
#     def post(self, *args, **kwargs):
#         try:
#             usuario = self.request.user
#             nombre = self.request.POST['nombre_can']
#             sexo = self.request.POST['sexo_can']
#             fecha = self.request.POST['fecha_can']
#             color = self.request.POST['color_can']
#             personalidad = self.request.POST['personalidad_can']
#             altura = self.request.POST['tamano_can']
#             nn = ""
#             file_path = [nn + x + "/" for x in
#                          str(TemporaryUploadedFile.temporary_file_path(self.request.FILES['foto_can'])).split('\\')]
#             nn = ""
#             for x in file_path:
#                 nn = nn + x
#             nn = nn[0:len(nn) - 1]
#             dato = nombre + str(fecha)
#             codigo = SubirArchivo(dato, nn)
#             foto_drive = "https://drive.google.com/uc?id=" + codigo
#             raza_nombre = self.request.POST['raza_can']
#             raza_id = Raza.objects.get(nombre=raza_nombre).id
#             nuevo_can = Can.objects.create(nombre=nombre, sexo=sexo, fecha_nacimiento=fecha, color=color,
#                                            foto_drive=foto_drive, codigo=codigo, personalidad=personalidad,
#                                            altura=altura,
#                                            id_raza_id=raza_id)
#             nuevo_can.save()
#             historial = HistorialUsuarios.objects.create(tipo="Registrando un nuevo can", usuario=usuario)
#             messages.success(self.request, 'Can registrado')
#         except ObjectDoesNotExist:
#             messages.error(self.request, 'Hubo algún error')
#         except IntegrityError:
#             messages.error(self.request, 'El can ya se encuentra registrado')
#         return redirect('vista_listar_can')

class AdminRegistroCan(SuperUsuarioMixin, View):
    def post(self, *args, **kwargs):
        try:
            usuario = self.request.user
            nombre = self.request.POST['nombre_can']
            sexo = self.request.POST['sexo_can']
            fecha = self.request.POST['fecha_can']
            color = self.request.POST['color_can']
            personalidad = self.request.POST['personalidad_can']
            altura = self.request.POST['tamano_can']
            raza_nombre = self.request.POST['raza_can']
            foto = self.request.FILES['foto_can']
            caso_independiente = self.request.POST['caso_independiente']
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$", caso_independiente)
            raza_id = Raza.objects.get(nombre=raza_nombre).id
            nuevo_can = Can.objects.create(nombre=nombre, sexo=sexo, fecha_nacimiento=fecha, color=color,
                                           personalidad=personalidad, altura=altura, foto=foto,
                                           caso_independiente=caso_independiente,
                                           id_raza_id=raza_id)
            nuevo_can.save()
            historial = HistorialUsuarios.objects.create(tipo="Registrando un nuevo can", usuario=usuario)
            messages.success(self.request, 'Can registrado correctamente')
        except ObjectDoesNotExist:
            messages.error(self.request, 'Hubo algún error')
        except IntegrityError:
            messages.error(self.request, 'El can ya se encuentra registrado')
        return redirect('vista_listar_can')


class AdminEditarCan(SuperUsuarioMixin, UpdateView):
    model = Can
    template_name = 'Administrador/Can/Editar/canes.html'
    form_class = FormCanEditar

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, *args, **kwargs):
        pk = self.kwargs['pk']
        usuario = self.request.user
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
        historial = HistorialUsuarios.objects.create(tipo="Actualizo los datos del can " + can.nombre, usuario=usuario)
        messages.success(self.request, "Can editado correctamente")
        return redirect('vista_listar_can')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        razas = Raza.objects.all()
        context['razas'] = razas
        return context


class AdminEliminarCan(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        usuario = self.request.user
        can = Can.objects.get(id=pk)
        historial = HistorialUsuarios.objects.create(tipo="Elimino los datos del can " + can.nombre, usuario=usuario)
        can.delete()
        messages.info(self.request, "Can eliminado correctamente")
        return redirect('vista_listar_can')


class AdminRegistrarEsterilizacion(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        can = Can.objects.get(id=pk)
        return render(self.request, 'Administrador/Can/Esterilizacion.html', {'can': can})

    def post(self, *args, **kwargs):
        pk = self.kwargs['pk']
        usuario = self.request.user
        can = Can.objects.get(id=pk)
        n_tattoo = self.request.POST['txtTattoo']
        fecha = self.request.POST['txtFecha']
        Esterilizacion.objects.create(n_tattoo=n_tattoo, fecha=fecha, cam_id=pk)
        can.esterilizado = True
        can.save()
        historial = HistorialUsuarios.objects.create(tipo="Asigno esterilización al can " + can.nombre, usuario=usuario)
        messages.success(self.request, 'Registro de esterilización correctamente')
        return redirect('vista_listar_can')


class AdminEditarEsterilizacion(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        esterilizacion = Esterilizacion.objects.get(cam_id=pk)
        return render(self.request, 'Administrador/Can/Editar/esterilizacion.html', {'esterilizacion': esterilizacion})

    def post(self, *args, **kwargs):
        pk = self.kwargs['pk']
        usuario = self.request.user
        n_tattoo = self.request.POST['txtTattoo']
        fecha = self.request.POST['txtFecha']
        esterilizacion = Esterilizacion.objects.get(id=pk)
        esterilizacion.n_tattoo = n_tattoo
        esterilizacion.fecha = fecha
        esterilizacion.save()
        historial = HistorialUsuarios.objects.create(
            tipo="Actualizo los datos de esterilizacion del can " + esterilizacion.cam.nombre,
            usuario=usuario)
        messages.success(self.request, 'Esterilización editada correctamente')
        return redirect('vista_listar_can')


class AdminListarRaza(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        razas = Raza.objects.all()
        return render(self.request, 'Administrador/Can/Razas.html', {'razas': razas})


class AdminRegistroRaza(SuperUsuarioMixin, View):
    def post(self, request):
        nombre = request.POST['race_can']
        usuario = self.request.user
        race = Raza.objects.create(nombre=nombre)
        historial = HistorialUsuarios.objects.create(tipo="Registro una nueva raza " + race.nombre, usuario=usuario)
        return redirect('vista_listar_raza')


class AdminEditarRaza(SuperUsuarioMixin, UpdateView):
    model = Raza
    template_name = 'Administrador/Can/Editar/raza.html'
    form_class = FormRazaEditar

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        nombre = form.cleaned_data['nombre']
        usuario = self.request.user
        messages.success(self.request, "Raza editado correctamente")
        historial = HistorialUsuarios.objects.create(tipo="Actualizo los datos de la raza " + nombre, usuario=usuario)
        return redirect('vista_listar_raza')


class AdminEliminarRaza(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        usuario = self.request.user
        raza = Raza.objects.get(id=pk)
        historial = HistorialUsuarios.objects.create(tipo="Elimino los datos de la raza " + raza.nombre,
                                                     usuario=usuario)
        raza.delete()
        messages.info(self.request, "Raza eliminado correctamente")
        return redirect('vista_listar_raza')


class AdminListarVacuna(SuperUsuarioMixin, View):
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


class AdminRegistrarVacuna(SuperUsuarioMixin, View):
    def post(self, *args, **kwargs):
        usuario = self.request.user
        nombre = self.request.POST['txtNombre']
        caracteristicas = self.request.POST['txtCaracteristicas']
        vacuna = Vacuna.objects.create(nombre=nombre, caracteristicas=caracteristicas)
        historial = HistorialUsuarios.objects.create(tipo="Registro una nueva vacuna " + vacuna.nombre, usuario=usuario)
        messages.success(self.request, 'Vacuna registrada correctamente')
        return redirect('vista_listar_vacuna')


class AdminAsignarVacuna(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        can = Can.objects.get(id=pk)
        vacunas = Vacuna.objects.all()
        return render(self.request, 'Administrador/Can/Registrar/vacunas_canes.html',
                      {'vacunas': vacunas, 'can': can})

    def post(self, *args, **kwargs):
        pk = self.kwargs['pk']
        usuario = self.request.user
        fecha = self.request.POST['txtFecha']
        vacuna = self.request.POST['txtVacuna']
        vacunas = Vacunas_Can.objects.create(fecha=fecha, can_id=pk, vacuna_id=vacuna)
        historial = HistorialUsuarios.objects.create(tipo="Asigno una vacuna al can " + vacunas.can.nombre,
                                                     usuario=usuario)
        messages.success(self.request, 'Vacuna asignada correctamente')
        return redirect('vista_listar_vacuna')


class AdminHistorialVacuna(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        can = Can.objects.get(id=pk)
        historiales = Vacunas_Can.objects.filter(can_id=pk).distinct()
        return render(self.request, 'Administrador/Can/Historial_vacunas.html',
                      {'historiales': historiales, 'can': can})


class AdminEliminarVacuna(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        usuario = self.request.user
        vacuna = Vacunas_Can.objects.get(id=pk)
        id_can = vacuna.can_id
        historial = HistorialUsuarios.objects.create(tipo="Elimino los datos de la vacuna " + vacuna.vacuna.nombre,
                                                     usuario=usuario)
        vacuna.delete()
        messages.info(self.request, "Vacuna eliminado correctamente")
        return redirect('vista_historial_vacuna', id_can)


class AdminEditarVacunaCan(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        vacuna_asignada = Vacunas_Can.objects.get(id=pk)
        vacunas = Vacuna.objects.all()
        return render(self.request, 'Administrador/Can/Editar/vacuna.html',
                      {'vacuna_asignada': vacuna_asignada, 'vacunas': vacunas})

    def post(self, *args, **kwargs):
        pk = self.kwargs['pk']
        usuario = self.request.user
        fecha = self.request.POST['txtFecha']
        vacuna = self.request.POST['txtVacuna']
        vacuna_can = Vacunas_Can.objects.get(id=pk)
        vacuna_can.fecha = fecha
        vacuna_can.vacuna_id = vacuna
        vacuna_can.save()
        id_can = vacuna_can.can_id
        historial = HistorialUsuarios.objects.create(
            tipo="Actualizo la asignación de vacuna del can" + vacuna_can.can.nombre, usuario=usuario)
        messages.success(self.request, 'Vacuna editada')
        return redirect('vista_historial_vacuna', id_can)


class AdminListarAdopciones(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        adoptadores = Usuario_Adoptivo.objects.all()
        return render(self.request, 'Administrador/Adopciones/adopciones.html', {'adoptadores': adoptadores})


class AdminRegistraAdopcion(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        canes = Can.objects.filter(adoptado=False, caso_independiente=False)
        adoptador = Usuario_Adoptivo.objects.get(id=pk)
        return render(self.request, 'Administrador/Adopciones/Registrar/adopcion.html',
                      {'canes': canes, 'adoptador': adoptador})

    def post(self, *args, **kwargs):
        try:
            pk = self.kwargs['pk']
            usuario = self.request.user
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
                historial = HistorialUsuarios.objects.create(tipo="Registro la adopción del can " + can.nombre,
                                                             usuario=usuario)
                messages.success(self.request, 'Adopción registrada correctamente')
            else:
                messages.info(self.request, 'La operación no se ejecuto correctamente')
        except ObjectDoesNotExist:
            messages.error(self.request, 'Hubo algún error')
        return redirect('vista_listar_adopciones')


class AdminListarACargo(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        adoptador = Usuario_Adoptivo.objects.get(id=pk)
        canes = Can.objects.filter(id_usuario_adoptivo=pk)
        return render(self.request, 'Administrador/Adopciones/a_cargo.html', {'adoptador': adoptador, 'canes': canes})


class AdminImprimirAdopcion(SuperUsuarioMixin, View):
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


class AdminEliminarAdopcion(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        us = self.request.user
        can = Can.objects.get(id=pk)
        id_usuario = can.id_usuario_adoptivo_id
        can.adoptado = False
        can.id_usuario_adoptivo_id = None
        can.save()
        usuario = Usuario_Adoptivo.objects.get(id=id_usuario)
        usuario.cantidad_max = usuario.cantidad_max - 1
        usuario.save()
        historial = HistorialUsuarios.objects.create(tipo="Elimino la adopción del can " + can.nombre, usuario=us)
        messages.info(self.request, 'Adopción retirada correctamente')
        return redirect('vista_listar_a_cargo', id_usuario)


class AdminListarReuniones(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        adoptadores = Usuario_Adoptivo.objects.all()
        return render(self.request, 'Administrador/Reuniones/reuniones.html', {'adoptadores': adoptadores})


class AdminRegistrarReuniones(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        adoptante = Usuario_Adoptivo.objects.get(id=pk)
        return render(self.request, 'Administrador/Reuniones/Registrar/reunion.html', {'adoptante': adoptante})

    def post(self, *args, **kwargs):
        try:
            pk = self.kwargs['pk']
            usuario = self.request.user
            usuario_adoptivo = Usuario_Adoptivo.objects.get(id=pk)
            fecha = self.request.POST['txtFecha']
            motivo = self.request.POST['txtMotivo']
            Reunion.objects.create(fecha=fecha, motivo=motivo, usuario_adoptivo_id=usuario_adoptivo.id)
            historial = HistorialUsuarios.objects.create(
                tipo="Registro una nueva visita al adoptante " + usuario_adoptivo.usuario.nombres + " " + usuario_adoptivo.usuario.apellidos,
                usuario=usuario)
            messages.info(self.request, 'Reunión registrada correctamente')
        except ObjectDoesNotExist:
            messages.error(self.request, 'Hubo algún error')
        return redirect('vista_listar_reuniones')


class AdminHistorialReuniones(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        adoptador = Usuario_Adoptivo.objects.get(id=pk)
        reuniones = Reunion.objects.filter(usuario_adoptivo_id=pk)
        return render(self.request, 'Administrador/Reuniones/Historiales_reuniones.html',
                      {'reuniones': reuniones, 'adoptador': adoptador})


class AdminEditarReunion(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        reunion = Reunion.objects.get(id=pk)
        return render(self.request, 'Administrador/Reuniones/Editar/editar.html', {'reunion': reunion})

    def post(self, *args, **kwargs):
        pk = self.kwargs['pk']
        usuario = self.request.user
        reunion = Reunion.objects.get(id=pk)
        fecha = self.request.POST['txtFecha']
        motivo = self.request.POST['txtMotivo']
        reunion.fecha = fecha
        reunion.motivo = motivo
        reunion.save()
        historial = HistorialUsuarios.objects.create(
            tipo="Altualizo los datos de la visita del adoptante " + reunion.usuario_adoptivo.usuario.apellidos + " " + reunion.usuario_adoptivo.usuario.nombres,
            usuario=usuario)
        messages.success(self.request, 'Visita editada correctamente')
        return redirect('vista_historial_reuniones', reunion.usuario_adoptivo_id)


class AdminEliminarReunion(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        try:
            pk = self.kwargs['pk']
            usuario = self.request.user
            reunion = Reunion.objects.get(id=pk)
            historial = HistorialUsuarios.objects.create(
                tipo="Elimino los datos de la visita " + reunion.usuario_adoptivo.usuario.apellidos + " " + reunion.usuario_adoptivo.usuario.nombres,
                usuario=usuario)
            reunion.delete()
            messages.info(self.request, 'Visita eliminada correctamente')
            return redirect('vista_historial_reuniones', reunion.usuario_adoptivo_id)
        except ObjectDoesNotExist:
            messages.error(self.request, 'Hubo algún error')
            return redirect('vista_listar_reuniones')


class AdminConfirmarReunion(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        reunion = Reunion.objects.get(id=pk)
        reunion.estado = True
        reunion.save()
        messages.info(self.request, 'Visita confirmada')
        return redirect('Administrador')


class SolicitarAdopcion(View):
    def get(self, *args, **kwargs):
        id_can = self.kwargs['pk']
        can = Can.objects.get(id=id_can)
        fecha_nacimiento = can.fecha_nacimiento
        edad = relativedelta(datetime.now(), fecha_nacimiento)
        return render(self.request, 'pages/vista_canes/adopcion..html', {'can': can, 'edad': edad})

    def post(self, *args, **kwargs):
        can = Can.objects.get(id=self.kwargs['pk'])
        try:
            nombres = self.request.POST['txtNombres']
            correo = self.request.POST['txtCorreo']
            celular = self.request.POST['txtCelular']
            name = str(nombres)
            email = correo
            subject = "Adopción"
            message = "Deseo solicitar la adopción de " + can.nombre
            template = loader.get_template('Administrador/Adopciones/adopciones_forms.txt')
            context = {
                'name': name,
                'email': email,
                'subject': subject,
                'message': message,
            }
            message = template.render(context)
            email = EmailMultiAlternatives(
                "Solicitud de adopción", message,
                "",
                ['hocicosdelmundo.adopciones@gmail.com']
            )
            email.content_subtype = 'html'
            email.send()
            Solicitud_Adopcion.objects.create(nombre_completo=nombres, celular=celular, correo=correo, nombre_can=can)
            print('envio correcto')
            messages.success(self.request,
                             "Solicitud enviada correctamente, el administrador se comunicara con usted a la brevedad "
                             "posible")
        except ObjectDoesNotExist:
            messages.error(self.request, 'Hubo algún error')
        return redirect('vista_solicitud_adopcion', can.id)
