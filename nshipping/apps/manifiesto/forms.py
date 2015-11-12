from django import forms
from django.forms.models import ModelMultipleChoiceField

from .models import Car, Driver, Manifest

from apps.ingreso.models import Dues, DepositSlip, Branch
from apps.profiles.models import Profile


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
    destination = forms.CharField(label='Destino', required=False)


class RegisterManifestForm(forms.ModelForm):
    class Meta:
        model = Manifest
        fields = ('driver', 'car', 'deposit_slip', 'destination')
        widgets = {
            'deposit_slip': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, user, *args, **kwargs):
        super(RegisterManifestForm, self).__init__(*args, **kwargs)
        perfil = Profile.objects.filter(user=user)[0]
        branch = perfil.branch
        self.fields['deposit_slip'].queryset = DepositSlip.objects.filter(
            commited=False,
            output=False,
            destination=branch,
        )
