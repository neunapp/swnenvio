from django import forms 
from django.forms.formsets import formset_factory

from .models import Branch, Client, DepositSlip, DetailDeposit, Dues
from apps.profiles.models import Profile 

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields=("__all__")
        
    
class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ("__all__")

class DetailForm(forms.ModelForm):
    # formulario para almacenar el detalle de productos en envio
    class Meta:
        model = DetailDeposit
        fields = ('count','description')
        widgets = {
            'description': forms.TextInput(attrs={'value':' '}),
        }

    def clean_count(self):
        cantidad = self.cleaned_data['count']
        if cantidad<1:
            print '========ingrese una cantidad valida=========='
            self.add_error('count','ingrese una cantidad valida')
        return cantidad
    def clean_description(self):
        descripcion = self.cleaned_data['description']
        if len(descripcion)<5:
            print '========ingrese un nombre de objeto valido==========='
            self.add_error('description','ingrese un nombre de objeto valido')
        return descripcion


class NotaIngresoForm(forms.Form):
    TIPO_COMPROBANTE = (
        ('sc', 'SC'),               
        ('boleta', 'Boleta'),
        ('factura', 'Factura'),
    )
    #campos para nemro seria
    serie = forms.CharField(label='Serie', initial='01')
    number = forms.CharField(label='Numero', initial='01')
    #campos para destino origen
    origin= forms.ModelChoiceField(queryset=None)
    destination = forms.ModelChoiceField(queryset=None)
    #campos para remitente
    sen_name = forms.CharField(label='Nombres',initial='neunapp01')
    sen_razonsocial = forms.CharField(label='Razon Social',initial='neunapp')
    sen_id = forms.CharField(label='Ruc/Dni:',initial='12345678')
    #campos para destinatario
    addr_name = forms.CharField(label='Nombres',initial='neunapp02')
    addr_razonsocial = forms.CharField(label='Razon Social',initial='neunapp empresa')
    addr_id = forms.CharField(label='Ruc/Dni',initial='12457812124')
    #campos para cuotas
    tipo = forms.ChoiceField(label='Boleta/Factura', choices=TIPO_COMPROBANTE)
    acuenta = forms.DecimalField(label='A Cuenta', max_digits=12, decimal_places=5,initial='100')
    por_cobrar = forms.DecimalField(label='Por Cobrar', max_digits=12, decimal_places=5,initial='100')
    total = forms.DecimalField(label='Total', max_digits=12, decimal_places=5,initial='200')

    def __init__(self,user,*args, **kwargs):
        #sobre escribios metodo init
        super(NotaIngresoForm, self).__init__(*args, **kwargs)
        self.fields['origin'].queryset = Profile.objects.filter(user=user)
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
            self.add_error('addr_id','el Dni o Ruc solo admiten 8 u 11 digitos')       
        else:
            return ide

""" Formulario Para Entrega de Productos """

class SearchForm(forms.Form):
    # formulario para busquedas por filtro
    serie = forms.CharField(label='Serie', required=False)
    number = forms.CharField(label='Numero', required=False)
    sender = forms.CharField(label='Remitente', required=False)
    addressee = forms.CharField(label='Destinatario', required=False)
    date = forms.CharField(label='Fecha', required=False,widget=forms.TextInput(attrs={'class': 'datepicker'}))

class DetailDeliverForm(forms.Form):
    # formulario para aplicar el descuento y elegir el tipo de pago
    TIPO_COMPROBANTE = (
        ('sc', 'SC'),
        ('boleta', 'Boleta'),
        ('factura', 'Factura'),
    )
    discount = forms.DecimalField(label='Descuento',max_digits=12, decimal_places=5,initial='10')
    tipo = forms.ChoiceField(label='Boleta/Factura', choices=TIPO_COMPROBANTE)

    def clean_discount(self):
        descuento = self.cleaned_data['discount']
        if descuento<0:
            raise forms.ValidationError("No puede Aplicar Descuentos Negativos")
        return descuento
            
    