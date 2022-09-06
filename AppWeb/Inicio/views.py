from django.shortcuts import render
from django.views.generic import View
from AppWeb.Modulos.Adoption.models import Person, Dog


class Index(View):
    def get(self, request):
        pk = self.request.user
        usuario = Person.objects.get(person_id=pk)
        return render(request, 'index.html', {'usuario': usuario})


class Administration(View):
    def get(self, request, **kwargs):
        pk = self.request.user
        usuario = Person.objects.get(person_id=pk)
        return render(request, 'Administrador/admin.html', {'usuario': usuario})


class PaginaAdopciones(View):
    def get(self, request):
        dogs = Dog.objects.filter(adopted=False)
        pk = self.request.user
        usuario = Person.objects.get(person_id=pk)
        return render(request, 'pages/adopciones.html', {'dogs': dogs, 'usuario': usuario})
