# -*- encoding: utf-8 -*-

from django import forms

from .models import Branch, Client, DepositSlip, Dues
from apps.profiles.models import Profile


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ("__all__")


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ("__all__")


class NotaIngresoForm(forms.ModelForm):
    '''
    Formulario de nota de ingreso para registrar
    nota de ingreso, clientes y la primera cuota
    '''
    sender_id = forms.CharField(
        label='Ruc/Dni',
        max_length=11,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm',
                'placeholder': 'Ingrese Dni o Ruc'
            }
        )
    )
    sender_name = forms.CharField(
        label='nombres',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm',
                'placeholder': 'Ingrese nombres completos'
            }
        )
    )
    sender_razonsocial = forms.CharField(
        label='razon social',
        max_length=50,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm',
                'placeholder': 'Ingrese nombre de la empresa'
            }
        )
    )
    # campos para destinatario
    addr_id = forms.CharField(
        label='Ruc/Dni',
        max_length=11,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm',
                'placeholder': 'Ingrese Dni o Ruc'
            }
        )
    )
    addr_name = forms.CharField(
        label='nombres',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm',
                'placeholder': 'Ingrese nombres completos'
            }
        )
    )
    addr_razonsocial = forms.CharField(
        label='razon Social',
        max_length=50,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm',
                'placeholder': 'Ingrese nombre de la empresa'
            }
        )
    )

    acuenta = forms.CharField(
        label='acuenta',
        max_length=50,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '0.0'
            }
        )
    )

    class Meta:
        model = DepositSlip
        fields = (
            'serie',
            'number',
            'origin',
            'voucher',
            'guide',
            'destination',
            'total_amount',
            'count',
            'description',
        )

        widgets = {
            'serie': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Serie'
                }
            ),
            'number': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Numero'
                }
            ),
            'voucher': forms.Select(
                attrs={'class': 'form-control input-sm'}
            ),
            'guide': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Nro de guia remitente'
                }
            ),
            'origin': forms.Select(
                attrs={'class': 'form-control input-sm'}
            ),
            'destination': forms.Select(
                attrs={'class': 'form-control input-sm'}
            ),
            'total_amount': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
            'count': forms.NumberInput(
                attrs={
                    'class': 'form-control input-sm input-detail',
                    'placeholder': '0',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control input-detail',
                    'placeholder': 'Ingrese descripción',
                    'rows': '4'
                }
            ),
        }

    def __init__(self, user, *args, **kwargs):
        super(NotaIngresoForm, self).__init__(*args, **kwargs)
        # recuperar todas las sucursales a las que pertenece el usuario
        # y las alamcenamos en la variable ids
        ids = [id.branch.id for id in Profile.objects.filter(user=user)]

        self.fields['origin'].queryset = Branch.objects.filter(id__in=ids)

    # realizamos validaciones
    def clean_serie(self):
        serie = self.cleaned_data['serie']
        if not serie.isdigit():
            raise forms.ValidationError("Ingrese solo numeros por favor")
        return serie

    def clean_number(self):
        numero = self.cleaned_data['number']
        if not numero.isdigit():
            raise forms.ValidationError("Ingrese solo numeros por favor")
        return numero

    def clean_sender_id(self):
        ide = self.cleaned_data['sender_id']
        if not ide.isdigit():
            msj = 'el Dni o Ruc solo deben contener numeros'
            self.add_error('sender_id', msj)
        elif len(ide) != 8 and len(ide) != 11:
            msj = 'el Dni o Ruc solo admiten 8 u 11 digitos'
            self.add_error('sender_id', msj)
        else:
            return ide

    def clean_addr_id(self):
        ide = self.cleaned_data['addr_id']
        if not ide.isdigit():
            msj = 'el Dni o Ruc solo deben contener numeros'
            self.add_error('addr_id', msj)
        elif len(ide) != 8 and len(ide) != 11:
            msj = 'el Dni o Ruc solo admiten 8 u 11 digitos'
            self.add_error('addr_id', msj)
        else:
            return ide

    # def clean_acuenta(self):
    #     acuenta = self.cleaned_data['acuenta']
    #     total = self.cleaned_data['total_amount']
    #     if not acuenta.isdigit():
    #         msj = 'Debe ser un numero'
    #         self.add_error('acuenta', msj)
    #     elif float(acuenta) < 0:
    #         msj = 'No puede ser negativo'
    #         self.add_error('acuenta', msj)
    #     elif acuenta > total:
    #         msj = 'No puede ser mayor al total'
    #         self.add_error('acuenta', msj)
    #     else:
    #         return acuenta

    # def clean_total_amount(self):
    #     total = self.cleaned_data['total_amount']
    #     if not total.isdigit():
    #         msj = 'Debe ser un numero'
    #         self.add_error('total_amount', msj)
    #     elif total < 0:
    #         msj = 'No puede ser negativo'
    #         self.add_error('total_amount', msj)
    #     else:
    #         return total


class SearchForm(forms.Form):
    # formulario para busquedas por filtro
    serie = forms.CharField(label='Serie', required=False)
    number = forms.CharField(label='Numero', required=False)
    sender = forms.CharField(label='Remitente', required=False)
    addressee = forms.CharField(label='Destinatario', required=False)
    date = forms.CharField(
        label='Fecha',
        required=False,
        widget=forms.TextInput(attrs={'class': 'datepicker'})
    )


class DetailDeliverForm(forms.Form):
    # formulario para aplicar el descuento y elegir el tipo de pago
    TIPO_COMPROBANTE = (
        ('sc', 'SC'),
        ('boleta', 'Boleta'),
        ('factura', 'Factura'),
    )
    discount = forms.DecimalField(
        label='Descuento',
        max_digits=12,
        decimal_places=5,
        initial='10'
    )
    tipo = forms.ChoiceField(
        label='Boleta/Factura',
        choices=TIPO_COMPROBANTE
    )

    def clean_discount(self):
        descuento = self.cleaned_data['discount']
        if descuento < 0:
            raise forms.ValidationError("No pede Aplicar Descuentos Negativos")
        return descuento
