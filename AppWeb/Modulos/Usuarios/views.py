from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import View, FormView, UpdateView
from .models import *
from .forms import *
from django.contrib import messages
from AppWeb.Modulos.Adopciones.models import *
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q
from AppWeb.Inicio.mixins import *


class AdminListarUsuarios(SuperUsuarioMixin, View):
    def get(self, request):
        search = request.GET.get('search')
        usuarios = User.objects.filter(is_superuser=True).values('id', 'nombres', 'apellidos', 'email')
        if search:
            usuarios = usuarios.filter(
                Q(nombres__icontains=search) |
                Q(apellidos__icontains=search) |
                Q(email__icontains=search)
            )
        return render(request, 'Administrador/Usuarios/Super_usuarios.html', {'usuarios': usuarios})


class AdminRegistroUsuarios(SuperUsuarioMixin, FormView):
    template_name = 'Administrador/Usuarios/Registros/usuario_admin.html'
    form_class = FormUsuarioRegistrar
    success_url = '/usuarios/listar'

    def form_valid(self, form):
        usuario = self.request.user
        super_usuario = User.objects.create_superuser(
            form.cleaned_data['email'],
            form.cleaned_data['password'],
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
        )
        historial = HistorialUsuarios.objects.create(
            tipo="Registro un nuevo super usuario " + super_usuario.nombres + " " + super_usuario.apellidos,
            usuario=usuario)
        return super(AdminRegistroUsuarios, self).form_valid(form)


class AdminEliminarUsuario(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        us = self.request.user
        usuario = User.objects.get(id=pk)
        historial = HistorialUsuarios.objects.create(
            tipo="Elimino los datos del usuario " + usuario.nombres + " " + usuario.apellidos, usuario=us)
        usuario.delete()
        messages.success(self.request, "Eliminado")
        return redirect('vista_listar_usuarios')


class LoginUsuarios(FormView):
    template_name = 'Administrador/Usuarios/Login/login.html'
    form_class = FormLoginUsuarios
    success_url = reverse_lazy('Administrador')

    def form_valid(self, form):
        usuario = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
        login(self.request, usuario)
        return super(LoginUsuarios, self).form_valid(form)


class LogoutUsuarios(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('Index'))


class AdminListarAdoptantes(SuperUsuarioMixin, View):
    def get(self, request):
        search = request.GET.get('search')
        adoptantes = Usuario_Adoptivo.objects.all()
        if search:
            adoptantes = adoptantes.filter(
                Q(usuario__nombres__icontains=search) |
                Q(usuario__apellidos__icontains=search) |
                Q(usuario__email__icontains=search)
            )
        return render(request, 'Administrador/Usuarios/Adoptantes.html', {'adoptantes': adoptantes})


class AdminRegistroAdoptantes(SuperUsuarioMixin, FormView):
    template_name = 'Administrador/Usuarios/Registros/usuario_adoptante.html'
    form_class = FormAdoptanteRegistrar
    success_url = '/usuarios/adoptantes/listar'

    def form_valid(self, form):
        usuario = self.request.user
        usuarios = User.objects.create_user(
            form.cleaned_data['email'],
            form.cleaned_data['password'],
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
            ci=form.cleaned_data['ci'],
            direccion=form.cleaned_data['direccion'],
            celular=form.cleaned_data['celular'],
        )
        usuarios.save()
        Usuario_Adoptivo.objects.create(cantidad_max=0, usuario_id=usuarios.id)
        historial = HistorialUsuarios.objects.create(
            tipo="Registro un nuevo adoptante " + usuarios.nombres + " " + usuarios.apellidos, usuario=usuario)
        return super(AdminRegistroAdoptantes, self).form_valid(form)


class AdminEditarAdoptante(SuperUsuarioMixin, UpdateView):
    model = User
    template_name = 'Administrador/Usuarios/Editar/usuario_adoptante.html'
    form_class = FormAdoptanteEditar
    success_url = reverse_lazy('vista_listar_adoptantes')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        usuario = self.request.user
        historial = HistorialUsuarios.objects.create(
            tipo="Actualizo los datos del usuario " + form.cleaned_data['nombres'] + " " + form.cleaned_data[
                'apellidos'], usuario=usuario)
        messages.success(self.request, "Adoptador editado")
        return redirect('vista_listar_adoptantes')


class AdminEliminarAdoptante(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        us = self.request.user
        usuario = User.objects.get(id=pk)
        historial = HistorialUsuarios.objects.create(
            tipo="Elimino los datos del adoptante " + usuario.nombres + " " + usuario.apellidos, usuario=us)
        usuario.delete()
        messages.info(self.request, "Adoptador eliminado")
        return redirect('vista_listar_adoptantes')


class AdminListarPadrinos(SuperUsuarioMixin, View):
    def get(self, request):
        search = request.GET.get('search')
        padrinos = User.objects.filter(is_padrino=True).values('id', 'nombres', 'apellidos', 'email', 'celular')
        if search:
            padrinos = padrinos.filter(
                Q(nombres__icontains=search) |
                Q(apellidos__icontains=search) |
                Q(email__icontains=search) |
                Q(celular__icontains=search)
            )
        return render(request, 'Administrador/Usuarios/Padrinos.html', {'padrinos': padrinos})


class AdminEditarPadrino(SuperUsuarioMixin, UpdateView):
    model = User
    template_name = 'Administrador/Usuarios/Editar/usuario_padrino.html'
    form_class = FormPadrinoEditar
    success_url = reverse_lazy('vista_listar_padrinos')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        usuario = self.request.user
        historial = HistorialUsuarios.objects.create(
            tipo="Actualizo los datos del padrino " + form.cleaned_data['nombres'] + " " + form.cleaned_data[
                'apellidos'], usuario=usuario)
        messages.success(self.request, "Padrino editado")
        return redirect('vista_listar_padrinos')


class AdminEliminarPadrino(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        us = self.request.user
        usuario = User.objects.get(id=pk)
        historial = HistorialUsuarios.objects.create(
            tipo="Elimino los datos del padrino " + usuario.nombres + " " + usuario.apellidos, usuario=us)
        usuario.delete()
        messages.info(self.request, "Padrino eliminado")
        return redirect('vista_listar_padrinos')


class AdminRegistroPadrinos(SuperUsuarioMixin, FormView):
    template_name = 'Administrador/Usuarios/Registros/usuario_padrino.html'
    form_class = FormPadrinoRegistrar
    success_url = '/usuarios/padrinos/listar'

    def form_valid(self, form):
        usuario = self.request.user
        padrino = User.objects.create_user(
            form.cleaned_data['email'],
            form.cleaned_data['password'],
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
            celular=form.cleaned_data['celular'],
            is_padrino=True,
        )
        historial = HistorialUsuarios.objects.create(
            tipo="Registro un nuevo padrino " + padrino.nombres + " " + padrino.apellidos, usuario=usuario)
        return super(AdminRegistroPadrinos, self).form_valid(form)


class AdminListarVoluntarios(SuperUsuarioMixin, View):
    def get(self, request):
        search = request.GET.get('search')
        voluntarios = User.objects.filter(is_voluntario=True)
        if search:
            voluntarios = voluntarios.filter(
                Q(nombres__icontains=search) |
                Q(apellidos__icontains=search) |
                Q(cargo__icontains=search)
            )
        return render(request, 'Administrador/Usuarios/Voluntatios.html', {'voluntarios': voluntarios})


class AdminRegistroVoluntarios(SuperUsuarioMixin, FormView):
    template_name = 'Administrador/Usuarios/Registros/usuario_voluntario.html'
    form_class = FormVoluntarioRegistrar
    success_url = reverse_lazy('vista_listar_voluntarios')

    def form_valid(self, form):
        usuario = self.request.user
        voluntario = User.objects.create_user(
            form.cleaned_data['email'],
            form.cleaned_data['password'],
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
            ci=form.cleaned_data['ci'],
            celular=form.cleaned_data['celular'],
            cargo=form.cleaned_data['cargo'],
            fecha_nacimiento=self.request.POST['txtFecha'],
            is_voluntario=True,
        )
        historial = HistorialUsuarios.objects.create(
            tipo="Registro un nuevo voluntario " + voluntario.nombres + " " + voluntario.apellidos, usuario=usuario)
        return super(AdminRegistroVoluntarios, self).form_valid(form)


class AdminEditarVoluntarios(SuperUsuarioMixin, UpdateView):
    model = User
    template_name = 'Administrador/Usuarios/Editar/usuario_voluntario.html'
    form_class = FormVoluntarioEditar
    success_url = reverse_lazy('vista_listar_voluntarios')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        usuario = self.request.user
        historial = HistorialUsuarios.objects.create(
            tipo="Actualizo los datos del voluntario " + form.cleaned_data['nombres'] + " " + form.cleaned_data[
                'apellidos'], usuario=usuario)
        messages.success(self.request, "Voluntario editado")
        return redirect('vista_listar_voluntarios')


class AdminEliminarVoluntarios(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        usuario = self.request.user
        voluntario = User.objects.get(id=pk)
        historial = HistorialUsuarios.objects.create(
            tipo="Elimino los datos del voluntario " + voluntario.nombres + " " + voluntario.apellidos, usuario=usuario)
        voluntario.delete()
        messages.info(self.request, "Voluntario eliminado")
        return redirect('vista_listar_voluntarios')
