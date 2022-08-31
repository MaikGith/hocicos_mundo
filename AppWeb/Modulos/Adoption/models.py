from django.db import models
from django.contrib.auth.models import User


class UserAdoptive(models.Model):
    person_adoptive = models.OneToOneField(User, on_delete=models.CASCADE)
    ci = models.CharField('Carnet de identidad', max_length=20)
    direccion = models.CharField('Dirección', max_length=254)
    cantidad_max = models.PositiveIntegerField('Cantidad de canes adoptados', default=0)


class Meeting(models.Model):
    person = models.ForeignKey(UserAdoptive, on_delete=models.CASCADE)
    date = models.DateField('Fecha de reunión')
    reason = models.CharField('Motivo de la reunión', max_length=250)


class Race(models.Model):
    name = models.CharField('Nombre de Raza', max_length=250)


class Vaccine(models.Model):
    name = models.CharField('Vacuna', max_length=250)
    features = models.CharField('características', max_length=250)


class Dog(models.Model):
    name = models.CharField('Nombre Can', max_length=250)
    specie = models.CharField('Especie', max_length=100)
    sex = models.CharField('Sexo', max_length=100)
    birth_date = models.DateField('Fecha de Nacimiento', blank=True)
    color = models.CharField('Color', max_length=100)
    personality = models.TextField('Personalidad', blank=True)
    size = models.CharField('Tamaño', max_length=250)
    race = models.ForeignKey(Race, null=True, on_delete=models.SET_NULL)
    photo = models.ImageField('Foto del can', upload_to="dogs_image", default=None)
    adopted = models.BooleanField('Estado de adopción', default=False)
    user_adoptive = models.ForeignKey(UserAdoptive, default=None, null=True, on_delete=models.SET_NULL)


class Vaccines(models.Model):
    vaccine = models.ForeignKey(Vaccine, null=True, on_delete=models.SET_NULL)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    date = models.DateField('Fecha de vacunación')


class Sterilization(models.Model):
    n_tattoo = models.CharField('Numero de tatuaje', max_length=50)
    date = models.DateField('Fecha de esterilización')
    dog = models.OneToOneField(Dog, on_delete=models.CASCADE)


class Sponsor(models.Model):
    user_sponsor = models.ForeignKey(User, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, null=True, on_delete=models.SET_NULL)
    date = models.DateField('Fecha de donación')
    monto = models.DecimalField('Monto de donación')


class Volunteers(models.Model):
    name = models.CharField('Nombre', max_length=250)
    last_name = models.CharField('Apellidos', max_length=250)
    ci = models.PositiveIntegerField('Carnet de identidad')
    user_charge = models.CharField('Cargo del voluntario', max_length=100)
    birth_date = models.DateField('Fecha de Nacimiento')
    authorization = models.ImageField()
