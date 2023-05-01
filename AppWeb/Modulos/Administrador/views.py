from django.shortcuts import render, redirect
from django.views.generic import View, FormView
from django.contrib import messages
from .models import *
from .forms import *
from AppWeb.Inicio.mixins import *
from AppWeb.Modulos.Usuarios.models import HistorialUsuarios
from django.db.models import Q


class AdminListarBlog(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        noticias = Blog.objects.all()
        return render(self.request, 'Administrador/Pagina/blog.html', {'noticias': noticias})


class AdminRegistrarBlog(SuperUsuarioMixin, FormView):
    template_name = 'Administrador/Pagina/registrar/Blog.html'
    form_class = FormBlogRegistrar
    success_url = '/admin_pagina/'

    def form_valid(self, form):
        usuario = self.request.user
        blog = Blog.objects.create(
            nombre_noticia=form.cleaned_data['nombre_noticia'],
            comentario=form.cleaned_data['comentario'],
            imagen=form.cleaned_data['imagen'],
            estado=form.cleaned_data['estado'],
            usuario_creador=usuario
        )
        historial = HistorialUsuarios.objects.create(
            tipo="Registro un nuevo blog" + blog.nombre_noticia, usuario=usuario)
        return super(AdminRegistrarBlog, self).form_valid(form)


class AdminEstadoBlog(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        usuario = self.request.user
        blog = Blog.objects.get(id=pk)
        blog.estado = not blog.estado
        blog.save()
        historial = HistorialUsuarios.objects.create(
            tipo="Actualizo el estado del blog" + blog.nombre_noticia, usuario=usuario)
        messages.info(self.request, 'Estado cambiado')
        return redirect('vista_listar_blog')


class AdminEditarBlog(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        id_blog = self.kwargs['pk']
        dato = Blog.objects.get(id=id_blog)
        form = FormBlogEditar(instance=dato)
        context = {'form': form, 'dato': dato}
        return render(self.request, 'Administrador/Pagina/editar/blog.html', context)

    def post(self, *args, **kwargs):
        id_blog = self.kwargs['pk']
        usuario = self.request.user
        dato = Blog.objects.get(id=id_blog)
        form = FormBlogEditar(self.request.POST, self.request.FILES, instance=dato)
        if form.is_valid():
            form.save()
        nombre = form.cleaned_data['nombre_noticia']
        historial = HistorialUsuarios.objects.create(
            tipo="Actualizo los datos del blog" + nombre, usuario=usuario)
        messages.success(self.request, "Blog editado")
        return redirect('vista_listar_blog')


class AdminEliminarBlog(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        usuario = self.request.user
        blog = Blog.objects.get(id=pk)
        historial = HistorialUsuarios.objects.create(
            tipo="Elimino los datos del blog" + blog.nombre_noticia, usuario=usuario)
        blog.delete()
        messages.info(self.request, "Blog eliminado")
        return redirect('vista_listar_blog')


class AdminListarMovimientos(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        search = self.request.GET.get('search')
        movimientos = HistorialUsuarios.objects.all()
        if search:
            movimientos = movimientos.filter(
                Q(tipo__icontains=search) |
                Q(usuario__nombres__icontains=search) |
                Q(usuario__apellidos__icontains=search)
            )
        return render(self.request, 'Administrador/Pagina/movimientos.html', {'movimientos': movimientos})


class AdminListarImagenes(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        imagenes = Inicio.objects.all()
        return render(self.request, 'Administrador/Pagina/imagenes.html', {'imagenes': imagenes})


class AdminRegistrarImagen(SuperUsuarioMixin, View):
    def post(self, *args, **kwargs):
        usuario = self.request.user
        nombre = self.request.POST['txtNombre']
        imagen = self.request.FILES['txtImagen']
        Inicio.objects.create(nombre=nombre, imagen=imagen)
        historial = HistorialUsuarios.objects.create(
            tipo="Registro una nueva imagen" + nombre, usuario=usuario)
        messages.success(self.request, 'Imagen registrada')
        return redirect('vista_listar_imagenes')


class AdminEditarImagen(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        id_imagen = self.kwargs['pk']
        dato = Inicio.objects.get(id=id_imagen)
        form = FormImagenEditar(instance=dato)
        context = {'form': form, 'dato': dato}
        return render(self.request, 'Administrador/Pagina/editar/imagenes.html', context)

    def post(self, *args, **kwargs):
        id_imagen = self.kwargs['pk']
        usuario = self.request.user
        dato = Inicio.objects.get(id=id_imagen)
        form = FormImagenEditar(self.request.POST, self.request.FILES, instance=dato)
        if form.is_valid():
            form.save()
        historial = HistorialUsuarios.objects.create(
            tipo="Actualizo los datos de la imagen", usuario=usuario)
        messages.success(self.request, "Imagen editada")
        return redirect('vista_listar_imagenes')


class AdminEliminarImagen(SuperUsuarioMixin, View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        usuario = self.request.user
        imagen = Inicio.objects.get(id=pk)
        historial = HistorialUsuarios.objects.create(
            tipo="Elimino los datos de la imagen" + imagen.nombre, usuario=usuario)
        imagen.delete()
        messages.info(self.request, "Imagen eliminada")
        return redirect('vista_listar_imagenes')
