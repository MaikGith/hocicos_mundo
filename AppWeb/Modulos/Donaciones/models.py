from django.db import models
from AppWeb.Modulos.Adopciones.models import Can
from AppWeb.Modulos.Usuarios.models import User


# Create your models here.
class Donador(models.Model):
    fecha = models.DateField('Fecha de donación')
    monto = models.DecimalField('Monto de donación', max_digits=12, decimal_places=2)
    usuario_donador = models.ForeignKey(User, on_delete=models.CASCADE)
    id_can = models.ForeignKey(Can, null=True, on_delete=models.SET_NULL)
