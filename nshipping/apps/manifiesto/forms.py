from django import forms

from .models import Car, Driver, Manifest


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ("__all__")


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("__all__")


class FilterForm(forms.Form):
    # formulario para busquedas por filtro
    destination = forms.CharField(label='Destino',required=False)
    