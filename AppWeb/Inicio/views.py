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


class Index(View):
    def get(self, request):
        return render(request, 'index.html')


class Administrador(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('Index')

    def get(self, request, **kwargs):
        return render(request, 'Administrador/administrador.html')


class Login(View):
    def get(self, request):
        return render(request, 'Administrador/login/login.html')


class PaginaAdopciones(View):
    def get(self, request):
        canes = Can.objects.filter(adoptado=False)
        return render(request, 'pages/adopciones.html', {'canes': canes})


class LoginFormView(FormView):
    template_name = 'Administrador/login/login.html'
    form_class = FormLogin
    success_url = reverse_lazy('Administrador')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(LoginFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginFormView, self).form_valid(form)


def logoutUser(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')
