from django.db import models
from AppWeb.Modulos.Adoption.models import Person, Dog


# Create your models here.
class Sponsor(models.Model):
    user_sponsor = models.ForeignKey(Person, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, null=True, on_delete=models.SET_NULL)
    date = models.DateField('Fecha de donación')
    monto = models.DecimalField('Monto de donación', max_digits=12, decimal_places=2)
