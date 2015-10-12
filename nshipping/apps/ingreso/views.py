from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from django.views.generic.edit import FormView
from django.forms.formsets import formset_factory
#herramientas nternas
from django.utils import timezone
from django.core.urlresolvers import reverse_lazy
# local.
from .models import Branch, Client, DepositSlip, DetailDeposit, Dues
from .forms import DetailForm, NotaIngresoForm, ClientForm
#aplicaciones locales

class RegisterClient(CreateView):
    template_name = 'ingreso/new_client'
    form_class = ClientForm
    success_url = '.'


class RegisterSlipView(FormView):
    form_class = NotaIngresoForm
    template_name = 'ingreso/slip.html'
    success_url = '.'

    def dni_ruc(self, cadena_id, cliente):
        #si la cadena contiene 11 caracteres gurdar en ruc
        if len(cadena_id)>=11:
            cliente.ruc = cadena_id
            cliente.save()
        else:
            #caso contrario se guardara en dni
            cliente.dni = cadena_id
            cliente.save() 

    def get_context_data(self, **kwargs):
        context = super(RegisterSlipView, self).get_context_data(**kwargs)
        context['objetos'] = formset_factory(DetailForm, extra=2,max_num=3)
        return context

    def form_valid(self, form):
        data = self.request 
        form_set = formset_factory(DetailForm, extra=2, max_num=3)        
        #recuperamos datos de remitente
        cliente_sen = Client(
                    full_name=form.cleaned_data['sen_name'],
                    business_name=form.cleaned_data['sen_razonsocial'],
                    )
        #guardamos remitente
        cliente_sen.save()
        #verificamos dni o ruc
        self.dni_ruc(form.cleaned_data['sen_id'],cliente_sen)
        #recuperamos datos de destinatario
        cliente_addr = Client(
                        full_name=form.cleaned_data['addr_name'],
                        business_name=form.cleaned_data['addr_razonsocial'],
                        )
        #guardamos destinatario
        cliente_addr.save()
        #verificamos dni o ruc
        self.dni_ruc(form.cleaned_data['addr_id'],cliente_addr)
        #recuperamos datos de NotaIngreso
        nota_ingreso = DepositSlip(
                        serie=form.cleaned_data['serie'],
                        number=form.cleaned_data['number'],
                        origin=form.cleaned_data['origin'],
                        destination=form.cleaned_data['destination'],
                        sender=cliente_sen,
                        addressee=cliente_addr,
                        date=timezone.now(),
                        total_amount=form.cleaned_data['total'],
                        )
        #guardamos nota de ingreso
        nota_ingreso.save()
        #variable para importe para una cuota
        importe = form.cleaned_data['acuenta']
        #variable para tipo
        tipo = form.cleaned_data['tipo']
        #varable para igv
        igv = 0
        #variable para sub total
        sub_total = 0
        #reuperamos datos de cuota
        #asignamos el tipo en una cadena para comparar
        cadena_tipo = 'factura'
        if tipo == cadena_tipo:
            igv = (importe/100) * 18
            sub_total = importe-igv
        else:
            igv = 0
            sub_total = importe
        #asignamos valores
        cuota = Dues(
                amount=importe,
                deposit_slip=nota_ingreso,
                date=timezone.now(),
                proof_type=tipo,
                igv=igv,
                sub_total=sub_total,
                 )
        #verificamos si la cuota cubre el monto total  
        #guardamos cuota
        cuota.save()
        #recuperamos datos para detalle de nota de ingreso (formset)
        ingreso_detalle = form_set(self.request.POST)
        for objeto in ingreso_detalle:
            if objeto.is_valid():
                detalle_ingreso = DetailDeposit(
                                    deposit_slip=nota_ingreso,
                                    description=objeto.cleaned_data['description'],
                                    count=objeto.cleaned_data['count'],
                                    been=False,
                                    user=self.request.user,
                                    )
                detalle_ingreso.save()

        return super(RegisterSlipView, self).form_valid(form)
