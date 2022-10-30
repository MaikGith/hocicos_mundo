from django import forms
from .models import *


class FormCanEditar(forms.ModelForm):
    class Meta:
        model = Can
        fields = (
            'nombre',
            'sexo',
            'color',
            'personalidad',
            'altura',
        )

        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese del can',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'sexo': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese sexo del can',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'color': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su color del can',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'personalidad': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su personalidad',
                    'required': 'True',
                    'autocomplete': 'off',
                    'rows': "5"
                }
            ),
            'altura': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su tamaño',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
        }


class FormRazaEditar(forms.ModelForm):
    class Meta:
        model = Raza
        fields = (
            'nombre',
        )

        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese raza',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
        }
