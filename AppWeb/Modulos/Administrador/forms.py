from django.forms import *
from django import forms
from .models import *


class FormBlogRegistrar(ModelForm, Form):

    class Meta:
        model = Blog
        fields = (
            'nombre_noticia',
            'comentario',
            'imagen',
            'estado',
        )
        widgets = {
            'imagen': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'required': 'True',
                }
            ),
        }


class FormImagenEditar(ModelForm):
    class Meta:
        model = Inicio
        fields = '__all__'


class FormBlogEditar(ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'
