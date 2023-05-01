from django import forms
from .models import Donador


class FormEditarDonacion(forms.ModelForm):
    class Meta:
        model = Donador
        fields = (
            'monto',
        )
        widgets = {
            'monto': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese un monto',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
        }
