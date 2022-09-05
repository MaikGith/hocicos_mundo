from django.shortcuts import render, redirect
from django.views.generic import View
from .models import *


class AdminListarDog(View):
    def get(self, request):
        dogs = Dog.objects.all()
        races = Race.objects.all()
        pk = self.request.user
        usuario = Person.objects.get(person_id=pk)
        return render(request, 'Administrador/Dog/Dogs.html', {'dogs': dogs, 'razas': races, 'usuario': usuario})


class AdminRegistroDog(View):
    def post(self, request):
        name = request.POST['nombre_can']
        specie = request.POST['especie_can']
        sex = request.POST['sexo_can']
        fecha = request.POST['fecha_can']
        color = request.POST['color_can']
        personality = request.POST['personalidad_can']
        size = request.POST['tamano_can']
        photo = request.FILES['foto_can']
        race = request.POST['raza_can']
        new_dog = Dog.objects.create(name=name, specie=specie, sex=sex, birth_date=fecha, color=color,
                                     personality=personality, size=size, photo=photo, race_id=race)
        new_dog.save()
        return redirect('vista_listar_dog')
