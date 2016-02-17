# -*- encoding: utf-8 -*-
from django import forms

from .models import Branch, Client, DepositSlip
from apps.profiles.models import Profile

from .functions import is_number


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ("__all__")


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = (
            'name',
            'address',
            'departamento',
            'provincia',
            'distrito',
            'phone'
        )

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese el nombre de la sucursal'
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese el dirección de la sucursal'
                }
            ),
            'departamento': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese el departamento de la sucursal'
                }
            ),
            'provincia': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese el provincia de la sucursal'
                }
            ),
            'distrito': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese el distrtio de la sucursal'
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese el telefono de cantacto'
                }
            ),
        }


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
                'ng-class':'vm.classender',
                'ng-change':'vm.ValidarID(vm.dni, "sender")',
                'placeholder': 'Ingrese Dni o Ruc',
                'ng-model':'vm.dni',
            }
        )
    )
    sender_name = forms.CharField(
        label='nombres',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm',
                'ng-click':'vm.RecuperarCliente(vm.dni,"sender")',
                'ng-model':'vm.name',
                'placeholder': 'Ingrese nombres completos',
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
                'ng-click':'vm.RecuperarCliente(vm.dni,"sender")',
                'ng-model':'vm.rs',
                'placeholder': 'Ingrese nombre de la empresa',
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
                'ng-class':'vm.clasaddr',
                'ng-change':'vm.ValidarID(vm.addr_id,"addr")',
                'placeholder': 'Ingrese Dni o Ruc',
                'ng-model':'vm.addr_id',
            }
        )
    )
    addr_name = forms.CharField(
        label='nombres',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm',
                'ng-click':'vm.RecuperarCliente(vm.addr_id,"addr")',
                'ng-model':'vm.addr_name',
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
                'ng-click':'vm.RecuperarClienteD(vm.addr_id,"addr")',
                'ng-model':'vm.addr_rs',
                'placeholder': 'Ingrese nombre de la empresa'
            }
        )
    )

    acuenta = forms.DecimalField(
        label='acuenta',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'ng-model':'vm.acuenta',
                'ng-change':'vm.CalcularMonto(vm.amount)',
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
                    'ng-class':'vm.classerie',
                    'ng-model':'vm.serie',
                    'ng-change':'vm.VelidarSerie(vm.serie, "serie")',
                    'placeholder': 'Serie'
                }
            ),
            'number': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'ng-class':'vm.clasnumero',
                    'ng-model':'vm.numero',
                    'ng-change':'vm.VelidarSerie(vm.numero, "numero")',
                    'placeholder': 'Numero'
                }
            ),
            'voucher': forms.Select(
                attrs={'class': 'form-control input-sm'}
            ),
            'guide': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'ng-class':'vm.clasguide',
                    'ng-model':'vm.guide',
                    'ng-change':'vm.VelidarSerie(vm.guide, "guide")',
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
                attrs={
                    'class': 'form-control',
                    'ng-model':'vm.amount',
                    'ng-change':'vm.CalcularMonto(vm.amount)',
                    'placeholder': '0.00',
                }
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

    def clean(self):
        cleaned_data = super(NotaIngresoForm, self).clean()
        serie = cleaned_data.get('serie')
        number = cleaned_data.get('number')
        ds = DepositSlip.objects.filter(serie=serie, number=number).exists()
        if ds:
            message = "la nota de ingreso %s - %s" % (serie, number)
            raise forms.ValidationError(message)
        return cleaned_data

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

    def clean_acuenta(self):
        acuenta = self.cleaned_data['acuenta']
        total = self.cleaned_data['total_amount']
        if not is_number(acuenta):
            msj = 'Debe ser un numero'
            self.add_error('acuenta', msj)
        elif float(acuenta) < 0:
            msj = 'No puede ser negativo'
            self.add_error('acuenta', msj)
        elif float(acuenta) > float(total):
            msj = 'No puede ser mayor al total'
            self.add_error('acuenta', msj)
        else:
            return acuenta

    def clean_total_amount(self):
        total = self.cleaned_data['total_amount']
        if not is_number(total):
            msj = 'Debe ser un numero'
            self.add_error('total_amount', msj)
        elif float(total) < 0:
            msj = 'No puede ser negativo'
            self.add_error('total_amount', msj)
        else:
            return total


class SearchForm(forms.Form):
    # formulario para busquedas por filtro
    serie = forms.CharField(
        label='serie',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm',
                'placeholder': 'serie',
            }
        )
    )
    number = forms.CharField(
        label='numero',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm',
                'placeholder': 'numero',
            }
        )
    )
    sender = forms.CharField(
        label='remitente',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm',
                'placeholder': 'Ingrese nombre del remitente',
            }
        )
    )
    addressee = forms.CharField(
        label='restinatario',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm',
                'placeholder': 'Ingrese nombres del destinatario',
            }
        )
    )
    date = forms.CharField(
        label='Fecha',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm datepicker',
                'placeholder': 'ingrese Fecha',
            }
        )
    )


class DetailDeliverForm(forms.Form):
    discount = forms.DecimalField(
        label='Descuento',
        max_digits=7,
        decimal_places=2,
        required=False,
        initial=0.00,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'ingrese descuento',
            }
        )
    )

    def clean_discount(self):
        descuento = self.cleaned_data['discount']
        if descuento < 0:
            raise forms.ValidationError("No puede aplicar descuento negativo")
        return descuento
