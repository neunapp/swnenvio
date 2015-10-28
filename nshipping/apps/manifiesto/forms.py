from django import forms
from django.forms.models import ModelMultipleChoiceField

from .models import Car, Driver, Manifest

from apps.ingreso.models import Dues, DepositSlip, Branch


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


class RegisterManifestForm(forms.ModelForm):
    class Meta:
        model = Manifest
        fields = ("__all__")
        widgets = {
            'deposit_slip': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, pk, *args, **kwargs):
        super(RegisterManifestForm, self).__init__(*args, **kwargs)
        branch = Branch.objects.get(pk=pk)
        self.fields['deposit_slip'].queryset = DepositSlip.objects.filter(commited=False, destination=branch)
        self.fields['car'].queryset = Car.objects.all()
        self.fields['driver'].queryset = Driver.objects.all()
        self.fields['destination'].queryset = Branch.objects.all()
        print '=====formulario termindado====='
