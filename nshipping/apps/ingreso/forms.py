from django import forms 
from django.forms.formsets import formset_factory

from .models import Branch, Client, DepositSlip, DetailDeposit, Dues
from apps.profiles.models import Profile 

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields=("__all__")
    

class DetailForm(forms.Form):
    # formulario para almacenar el detalle de productos en envio
    count = forms.IntegerField(label='Cantidad')
    description = forms.CharField(label='Descripcion')

    def clean_count(self):
        cantidad = self.cleaned_data['count']
        if cantidad<1:
            print '========validacion cantidad=========='
            ValidationError("ingrese una cantidad valida")
        return cantidad
    def clean_description(self):
        descripcion = self.cleaned_data['description']
        if len(descripcion)<2:
            ValidationError("Descripcion de producto muy corto")
        return descripcion


class NotaIngresoForm(forms.Form):
    TIPO_COMPROBANTE = (
        ('boleta', 'Boleta'),
        ('factura', 'Factura'),
    )
    #campos para nemro seria
    serie = forms.CharField(label='Serie')
    number = forms.CharField(label='Numero')
    #campos para destino origen
    origin= forms.ModelChoiceField(queryset=None)
    destination = forms.ModelChoiceField(queryset=None)
    #campos para remitente
    sen_name = forms.CharField(label='Nombres')
    sen_razonsocial = forms.CharField(label='Razon Social')
    sen_id = forms.CharField(label='Ruc/Dni:')
    #campos para destinatario
    addr_name = forms.CharField(label='Nombres')
    addr_razonsocial = forms.CharField(label='Razon Social')
    addr_id = forms.CharField(label='Ruc/Dni')
    #campos para cuotas
    tipo = forms.ChoiceField(label='Boleta/Factura', choices=TIPO_COMPROBANTE)
    acuenta = forms.DecimalField(label='A Cuenta', max_digits=12, decimal_places=5)
    por_cobrar = forms.DecimalField(label='Por Cobrar', max_digits=12, decimal_places=5)
    total = forms.DecimalField(label='Total', max_digits=12, decimal_places=5)

    def __init__(self,*args, **kwargs):
        #sobre escribios metodo init
        super(NotaIngresoForm, self).__init__(*args, **kwargs)
        self.fields['origin'].queryset = Branch.objects.all()
        self.fields['destination'].queryset = Branch.objects.all()
    #realizamos validaciones
    def clean_serie(self):
        ser = self.cleaned_data['serie']
        if not ser.isdigit():
            raise forms.ValidationError("la Serie no puede contener letras :(")
        return ser
    #validamos el numero
    def clean_number(self):
        numero = self.cleaned_data['number']
        if not numero.isdigit():
            raise forms.ValidationError("un numero no puede contener letras :(")
        return numero 
    #validamos el dni o ruc
    def clean_sen_id(self):
        ide = self.cleaned_data['sen_id']
        if not ide.isdigit():
            self.add_error('sen_id','el Dni o Ruc no puede contener letras')
        elif len(ide) != 8 and len(ide) != 11:
            self.add_error('sen_id','el Dni o Ruc solo admiten 8 u 11 digitos')       
        else:
            return ide
            
    def clean_addr_id(self):
        ide = self.cleaned_data['addr_id']
        if not ide.isdigit():
            self.add_error('addr_id','el Dni o Ruc no puede contener letras')
        elif len(ide) != 8 and len(ide) != 11:
            self.add_error('addr_id','el Dni o Ruc solo admiten 6 u 11 digitos')       
        else:
            return ide