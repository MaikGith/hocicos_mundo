from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import View, TemplateView
from AppWeb.Modulos.Adopciones.models import Can
from django.contrib.auth.mixins import LoginRequiredMixin
# # librerias para la seguridad de la página
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout
from django.views.generic.edit import FormView
from .forms import FormLogin
from AppWeb.Modulos.Adopciones.models import Raza, Reunion
from AppWeb.Modulos.Perdidos.models import Perdido
from AppWeb.Modulos.Administrador.models import *
from django.core.paginator import Paginator
from django.http import Http404
from AppWeb.Inicio.mixins import *
from datetime import datetime
from dateutil.relativedelta import relativedelta


class Index(View):
    def get(self, *args, **kwargs):
        imagenes = Inicio.objects.filter(nombre__icontains="portada")
        return render(self.request, 'index.html', {'imagenes': imagenes})


class Administrador(SuperUsuarioMixin, TemplateView):
    def get(self, request, **kwargs):
        reuniones = Reunion.objects.filter(estado=False)
        return render(request, 'Administrador/administrador.html', {'reuniones': reuniones})


class PaginaAdopciones(View):
    def get(self, *args, **kwargs):
        canes = Can.objects.filter(adoptado=False, estado=True)
        razas = Raza.objects.all()
        raza = self.request.GET.get('txtRaza')
        altura = self.request.GET.get('txtAltura')
        sexo = self.request.GET.get('txtSexo')
        if raza:
            if raza != "0":
                canes = canes.filter(id_raza=raza)
        if altura:
            if altura != "":
                canes = canes.filter(altura=altura)
        if sexo:
            if sexo != "":
                canes = canes.filter(sexo=sexo)
        page = self.request.GET.get('page', 1)
        try:
            paginator = Paginator(canes, 6)
            canes = paginator.page(page)
        except:
            raise Http404
        return render(self.request, 'pages/adopciones.html', {'canes': canes, 'razas': razas, 'paginator': paginator})


class PaginaPadrinaje(View):
    def get(self, *args, **kwargs):
        canes = Can.objects.filter(adoptado=False, estado=True)
        razas = Raza.objects.all()
        raza = self.request.GET.get('txtRaza')
        altura = self.request.GET.get('txtAltura')
        sexo = self.request.GET.get('txtSexo')
        if raza:
            if raza != "0":
                canes = canes.filter(id_raza=raza)
        if altura:
            if altura != "":
                canes = canes.filter(altura=altura)
        if sexo:
            if sexo != "":
                canes = canes.filter(sexo=sexo)
        page = self.request.GET.get('page', 1)
        try:
            paginator = Paginator(canes, 6)
            canes = paginator.page(page)
        except:
            raise Http404
        return render(self.request, 'pages/apadrinar.html', {'canes': canes, 'razas': razas, 'paginator': paginator})


class PaginaPerdidos(View):
    def get(self, *args, **kwargs):
        canes = Perdido.objects.all()
        search = self.request.GET.get('search')
        if search:
            canes = canes.filter(can_perdido__nombre__contains=search)
        page = self.request.GET.get('page', 1)
        try:
            paginator = Paginator(canes, 6)
            canes = paginator.page(page)
        except:
            raise Http404
        return render(self.request, 'pages/perdidos.html', {'canes': canes, 'paginator': paginator})


class InformacionPerdido(View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        can = Can.objects.get(id=pk)
        perdido = Perdido.objects.get(can_perdido_id=pk)
        fecha_nacimiento = can.fecha_nacimiento
        edad = relativedelta(datetime.now(), fecha_nacimiento)
        return render(self.request, 'pages/vista_canes/perdido.html', {'can': can, 'perdido': perdido, 'edad': edad})


class PaginaBlog(View):
    def get(self, *args, **kwargs):
        blogs = Blog.objects.filter(estado=True)
        noticia = self.request.GET.get('noticia')
        if noticia:
            blogs = blogs.filter(nombre_noticia__icontains=noticia)
        page = self.request.GET.get('page', 1)
        try:
            paginator = Paginator(blogs, 3)
            blogs = paginator.page(page)
        except:
            raise Http404
        return render(self.request, 'pages/blog.html', {'blogs': blogs, 'paginator': paginator})


class PaginaBlogContenido(View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        blog = Blog.objects.get(id=pk)
        return render(self.request, 'pages/blog_contenido.html', {'blog': blog})


class PaginaQuienesSomos(View):
    def get(self, *args, **kwargs):
        imagenes = Inicio.objects.filter(nombre__icontains="somos")
        return render(self.request, 'pages/nosotros.html', {'imagenes': imagenes})
