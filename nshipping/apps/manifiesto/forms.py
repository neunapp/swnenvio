# -*- encoding: utf-8 -*-
from django import forms
from django.forms.models import ModelMultipleChoiceField

from .models import Car, Driver, Manifest

from apps.ingreso.models import Dues, DepositSlip, Branch
from apps.profiles.models import Profile


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ("__all__")

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese una Denominacion'
                }
            ),
            'plaque': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese Nro de Placa'
                }
            ),
            'marca': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese Marca del Vehiculo'
                }
            ),
            'code_ssettings_car': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese Codigo de Configuracion Vehicular'
                }
            ),
            'constancy_inscription': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese Nro de Cosntacia de Inscripcion'
                }
            ),
            'condition': forms.Select(
                attrs={'class': 'form-control input-sm'}
            ),
        }


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("__all__")

        widgets = {
            'dni': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese Nro de DNI'
                }
            ),
            'full_name': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese Nombre Completo'
                }
            ),
            'license': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese Nro de Licencia de Conducir'
                }
            ),
            'addreess': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese una Direccion'
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrse Nro de Telefono o Celular'
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese Direccion de Correo Electronico'
                }
            ),

            'date_birth': forms.DateInput(
                attrs={
                    'class': 'form-control input-sm datepicker',
                    'placeholder': 'Seleccione un fecha'
                },
                format='%d/%m/%Y'
            ),
        }

    def clean_dni(self):
        dni = self.cleaned_data['dni']
        if not dni.isdigit():
            msj = 'el Dni solo deben contener numeros'
            self.add_error('dni', msj)
        elif len(dni) != 8:
            msj = 'el Dni solo puede tener 8 digitos'
            self.add_error('dni', msj)
        else:
            return dni


class FilterForm(forms.Form):
    # formulario para busquedas por filtro
    destination = forms.CharField(label='Destino', required=False)


class ManifestForm(forms.ModelForm):
    """ Formulario para el Registro de Manifiesto"""
    class Meta:
        model = Manifest
        fields = (
            'driver',
            'car',
            'destination',
            'origin',
            'date_shipping',
        )

        widgets = {
            'driver': forms.Select(
                attrs={'class': 'form-control input-sm'}
            ),
            'car': forms.Select(
                attrs={'class': 'form-control input-sm'}
            ),
            'destination': forms.Select(
                attrs={'class': 'form-control input-sm'}
            ),
            'origin': forms.Select(
                attrs={'class': 'form-control input-sm'}
            ),
            'date_shipping': forms.DateInput(
                attrs={
                    'class': 'form-control input-sm datepicker',
                    'placeholder': 'Seleccione una fecha'
                },
                format='%d/%m/%Y'
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ManifestForm, self).__init__(*args, **kwargs)
        self.fields['car'].queryset = Car.objects.filter(
            condition='0',
            canceled=False
        )
        self.fields['driver'].queryset = Driver.objects.filter(
            canceled=False,
        )


class ThirdManifestForm(ManifestForm):
    """
    Formulario para el Registro de Manifiesto
    """
    full_name = forms.CharField(
        label='Nombres/RazonSocial',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-detail',
                'placeholder': 'Ingrese nombres o razón social',
            }
        ),
    )
    ruc = forms.CharField(
        label='Ruc',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-detail',
                'placeholder': 'Ingrese numero de ruc',
            }
        ),
    )
    observations = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control input-detail',
                'placeholder': 'Ingrese observación',
                'rows': '4'
            }
        ),
    )

    class Meta(ManifestForm.Meta):
        model = Manifest
        fields = (
            'driver',
            'car',
            'destination',
            'origin',
            'date_shipping',
        )

    def __init__(self, *args, **kwargs):
        super(ThirdManifestForm, self).__init__(*args, **kwargs)
        self.fields['car'].queryset = Car.objects.filter(
            condition='1',
            canceled=False
        )
        self.fields['driver'].queryset = Driver.objects.filter(
            canceled=False,
        )

    def clean_ruc(self):
        ruc = self.cleaned_data['ruc']
        if not ruc.isdigit():
            msj = 'el Ruc solo deben contener numeros'
            self.add_error('ruc', msj)
        elif len(ruc) != 11:
            msj = 'el Ruc solo puede tener 11 digitos'
            self.add_error('ruc', msj)
        else:
            return ruc


class RemissionForm(forms.Form):
    manifest = forms.ModelChoiceField(
        label='Manifiesto',
        queryset=None,
        widget=forms.Select(
            attrs={
                'class': 'form-control input-sm',
                'placeholder': 'Pulse para Seleccionar',
            }
        ),
    )

    def __init__(self, user, pk, *args, **kwargs):
        super(RemissionForm, self).__init__(*args, **kwargs)
        sucursal = Profile.objects.get(user=user).branch
        self.fields['manifest'].queryset = Manifest.objects.filter(
            state=False,
            origin=sucursal,
            canceled=False,
        )


# formulario para recepcionar notas de ingreso
class ReceptionForm(forms.Form):
    deposit_slip = forms.ModelMultipleChoiceField(
        queryset=None,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, pk, user, *args, **kwargs):
        super(ReceptionForm, self).__init__(*args, **kwargs)
        # recupera sucursal
        branch = Profile.objects.get(user=user).branch.id
        print branch
        # realizamos la consulta
        deposit_slip = DepositSlip.objects.slip_by_manifest(
            pk,
            branch,
        )
        print deposit_slip
        # asignamos la consulta
        self.fields['deposit_slip'].queryset = deposit_slip
        self.fields['deposit_slip'].label_from_instance = \
            lambda obj: "%s %s - %s - %s - %s - %s" % (
                obj.number,
                obj.serie,
                obj.origin,
                obj.sender,
                obj.addressee,
                obj.destination,
            )
        print self.fields['deposit_slip']
