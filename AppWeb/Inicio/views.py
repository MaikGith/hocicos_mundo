from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User
from AppWeb.Modulos.Adoption.models import Person


class Index(View):
    @staticmethod
    def get(request):
        return render(request, 'index.html')


class Administration(View):
    def get(self, request, **kwargs):
        pk = self.request.user
        usuario = Person.objects.get(person_id=pk)
        return render(request, 'Administrador/admin.html', {'usuario': usuario})
