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


# Create your views here.


class AdminListarUsuarios(View):
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


class AdminRegistroUsuarios(FormView):
    template_name = 'Administrador/Usuarios/Registros/usuario_admin.html'
    form_class = FormUsuarioRegistrar
    success_url = '/usuarios/listar'

    def form_valid(self, form):
        User.objects.create_superuser(
            form.cleaned_data['email'],
            form.cleaned_data['password'],
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
        )
        return super(AdminRegistroUsuarios, self).form_valid(form)


class AdminEliminarUsuario(View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        usuario = User.objects.get(id=pk)
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


class AdminListarAdoptantes(View):
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


class AdminRegistroAdoptantes(FormView):
    template_name = 'Administrador/Usuarios/Registros/usuario_adoptante.html'
    form_class = FormAdoptanteRegistrar
    success_url = '/usuarios/adoptantes/listar'

    def form_valid(self, form):
        usuarios = User.objects.create_user(
            form.cleaned_data['email'],
            form.cleaned_data['password'],
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
            ci=form.cleaned_data['ci'],
            direccion=form.cleaned_data['direccion'],
        )
        usuarios.save()
        Usuario_Adoptivo.objects.create(cantidad_max=0, usuario_id=usuarios.id)
        return super(AdminRegistroAdoptantes, self).form_valid(form)


class AdminEditarAdoptante(UpdateView):
    model = User
    template_name = 'Administrador/Usuarios/Editar/usuario_adoptante.html'
    form_class = FormAdoptanteEditar
    success_url = reverse_lazy('vista_listar_adoptantes')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Adoptador editado")
        return redirect('vista_listar_adoptantes')


class AdminEliminarAdoptante(View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        usuario = User.objects.get(id=pk)
        usuario.delete()
        messages.info(self.request, "Adoptador eliminado")
        return redirect('vista_listar_adoptantes')


class AdminListarPadrinos(View):
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


class AdminEditarPadrino(UpdateView):
    model = User
    template_name = 'Administrador/Usuarios/Editar/usuario_padrino.html'
    form_class = FormPadrinoEditar
    success_url = reverse_lazy('vista_listar_padrinos')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Padrino editado")
        return redirect('vista_listar_padrinos')


class AdminEliminarPadrino(View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        usuario = User.objects.get(id=pk)
        usuario.delete()
        messages.info(self.request, "Padrino eliminado")
        return redirect('vista_listar_padrinos')


class AdminRegistroPadrinos(FormView):
    template_name = 'Administrador/Usuarios/Registros/usuario_padrino.html'
    form_class = FormPadrinoRegistrar
    success_url = '/usuarios/padrinos/listar'

    def form_valid(self, form):
        User.objects.create_user(
            form.cleaned_data['email'],
            form.cleaned_data['password'],
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
            celular=form.cleaned_data['celular'],
            is_padrino=True,
        )
        return super(AdminRegistroPadrinos, self).form_valid(form)


class AdminListarVoluntarios(View):
    def get(self, request):
        search = request.GET.get('search')
        voluntarios = Voluntarios.objects.all()
        if search:
            voluntarios = voluntarios.filter(
                Q(nombres__icontains=search) |
                Q(apellidos__icontains=search) |
                Q(cargo__icontains=search)
            )
        return render(request, 'Administrador/Usuarios/Voluntatios.html', {'voluntarios': voluntarios})


class AdminRegistroVoluntarios(View):
    def get(self, *args, **kwargs):
        voluntarios = Voluntarios.objects.all()
        return render(self.request, 'Administrador/Usuarios/Registros/usuario_voluntario.html',
                      {'voluntarios': voluntarios})

    def post(self, *args, **kwargs):
        nombres = self.request.POST['txtNombres']
        apellidos = self.request.POST['txtApellidos']
        ci = self.request.POST['txtCi']
        cargo = self.request.POST['txtCargo']
        fecha_nac = self.request.POST['txtFecha']
        Voluntarios.objects.create(nombres=nombres, apellidos=apellidos, ci=ci, cargo=cargo, fecha_nacimiento=fecha_nac)
        messages.success(self.request, 'Voluntario registrado')
        return redirect('vista_listar_voluntarios')


class AdminEditarVoluntarios(UpdateView):
    model = Voluntarios
    template_name = 'Administrador/Usuarios/Editar/usuario_voluntario.html'
    form_class = FormVoluntarioEditar
    success_url = reverse_lazy('vista_listar_voluntarios')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Voluntario editado")
        return redirect('vista_listar_voluntarios')


class AdminEliminarVoluntarios(View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        voluntario = Voluntarios.objects.get(id=pk)
        voluntario.delete()
        messages.info(self.request, "Voluntario eliminado")
        return redirect('vista_listar_voluntarios')
