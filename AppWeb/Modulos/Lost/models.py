from django.db import models
from AppWeb.Modulos.Adoption.models import Dog


class Stray(models.Model):
    lost_dog = models.OneToOneField(Dog, null=True, on_delete=models.SET_NULL)
    lost_date = models.DateField('Fecha de perdida')
    state_found = models.BooleanField('Estado de encontrado', default=False)
    comments = models.TextField('Comentario')
