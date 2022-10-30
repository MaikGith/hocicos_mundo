import json
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
import requests


class VistaDonaciones(TemplateView):
    template_name = 'Administrador/Donaciones/donaciones.html'


class VistaDonar(View):
    def post(self, *args, **kwargs):
        url = 'https://botonpagoapiv1.azurewebsites.net/api/v1/main/getPaymentButton'
        foto = self.request.POST['txtFoto']
        datos = {
            "photo": "yJ2ZNYNk/kai3YCXD4hoNg==", "title": "Camisas",
            "detail": "Camisas Ejecutivas, Talla M , Colores Rojo y Blanco",
            "currency": "BOB",
            "amount": 123
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        r = requests.post(url, headers=headers, data=json.dumps(datos))
        print(r.json())
        return redirect('vista_donaciones')
