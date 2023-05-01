from django import forms
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate


class FormUsuarioRegistrar(forms.ModelForm):
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese contraseña'
            }
        )
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Reingrese contraseña'
            }
        )
    )

    class Meta:
        model = User
        fields = (
            'email',
            'nombres',
            'apellidos',
        )
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese un email',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'nombres': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese sus nombres',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese sus apellidos',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
        }

    def clean_password1(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password'] or len(
                str(self.cleaned_data['password'])) <= 6:
            self.add_error('password1', 'La contraseña es muy corta o no son iguales')


class FormLoginUsuarios(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su correo electronico',
                'autocomplete': 'off',
            }
        )
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su contraseña'
            }
        )
    )

    def clean(self):
        cleaned_data = super(FormLoginUsuarios, self).clean()
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not authenticate(email=email, password=password):
            self.add_error('password', 'Los datos son incorrectos')
        return self.cleaned_data


class FormAdoptanteRegistrar(forms.ModelForm):
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese contraseña'
            }
        )
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Reingrese contraseña'
            }
        )
    )

    class Meta:
        model = User
        fields = (
            'email',
            'nombres',
            'apellidos',
            'ci',
            'direccion',
            'celular',
        )
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese un email',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'nombres': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese sus nombres',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese sus apellidos',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'ci': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese carnet de identidad',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'direccion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su dirección',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'celular': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese número de celular',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
        }

    def clean_password1(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password'] or len(
                str(self.cleaned_data['password'])) <= 6:
            self.add_error('password1', 'La contraseña es muy corta o no son iguales')


class FormPadrinoRegistrar(forms.ModelForm):
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese contraseña'
            }
        )
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Reingrese contraseña'
            }
        )
    )

    class Meta:
        model = User
        fields = (
            'email',
            'nombres',
            'apellidos',
            'celular'
        )
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese un email',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'nombres': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese sus nombres',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese sus apellidos',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'celular': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese numero de celular',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
        }

    def clean_password1(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password'] or len(
                str(self.cleaned_data['password'])) <= 6:
            self.add_error('password1', 'La contraseña es muy corta o no son iguales')


class FormVoluntarioEditar(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'nombres',
            'apellidos',
            'ci',
            'celular',
            'cargo',
            'fecha_nacimiento'
        )
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese un email',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'nombres': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese sus nombres',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese sus apellidos',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'ci': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese carnet de identidad',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'celular': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese numero de celular',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'direccion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su dirección',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'cargo': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su cargo',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'fecha_nacimiento': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese carnet de identidad',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
        }


class FormAdoptanteEditar(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'nombres',
            'apellidos',
            'ci',
            'direccion',
            'celular',
        )
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese un email',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'nombres': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese sus nombres',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese sus apellidos',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'ci': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese carnet de identidad',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'direccion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su dirección',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'celular': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese numero de celular',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
        }


class FormPadrinoEditar(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'nombres',
            'apellidos',
            'celular'
        )
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese un email',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'nombres': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese sus nombres',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese sus apellidos',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'celular': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese numero de celular',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
        }


class FormVoluntarioRegistrar(forms.ModelForm):
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese contraseña'
            }
        )
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Reingrese contraseña'
            }
        )
    )

    class Meta:
        model = User
        fields = (
            'email',
            'nombres',
            'apellidos',
            'ci',
            'celular',
            'cargo',
            'fecha_nacimiento'
        )
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese un email',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'nombres': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese sus nombres',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese sus apellidos',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'ci': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese carnet de identidad',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'celular': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese numero de celular',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'direccion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su dirección',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'cargo': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su cargo',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
            'fecha_nacimiento': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese carnet de identidad',
                    'required': 'True',
                    'autocomplete': 'off',
                }
            ),
        }

    def clean_password1(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password'] or len(
                str(self.cleaned_data['password'])) <= 6:
            self.add_error('password1', 'La contraseña es muy corta o no son iguales')
