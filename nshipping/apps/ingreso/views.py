# -*- encoding: utf-8 -*-

from django.views.generic import TemplateView, DetailView, UpdateView
from django.views.generic.edit import CreateView, FormView, FormMixin
from django.views.generic.list import ListView
from django.forms.formsets import formset_factory
from django.utils import timezone
from datetime import datetime
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect

# local.
from .functions import ClientGetOrCreate
from .models import Branch, Client, Dues
from .forms import (
    DetailForm,
    NotaIngresoForm,
    ClientForm,
    SearchForm,
    DetailDeliverForm,
    BranchForm
)
#importamos la base de datos de Profile
from apps.profiles.models import Profile
#aplicaciones locales


#Mantenimiento de ciudades
class ListBranch(ListView):
    context_object_name = 'sucursales'
    queryset = Branch.objects.all()
    template_name = 'ingreso/sucursales/list.html'


class RegisterBranch(CreateView):
    template_name = 'ingreso/sucursales/add.html'
    form_class = BranchForm
    success_url = '.'


class UpdateBranch(UpdateView):
    #matenimietno actualiza carro
    model = Branch
    template_name = 'ingreso/sucursales/update.html'
    form_class = BranchForm
    success_url = reverse_lazy('ingreso_app:listar-branch')


class RegisterClient(CreateView):
    template_name = 'ingreso/new_client'
    form_class = ClientForm
    success_url = '.'


class ErrorView(TemplateView):
    template_name = 'ingreso/errors.html'


class DepositSlipView(FormView):
    '''
    vista para en registro de la nota de ingreso
    '''
    form_class = NotaIngresoForm
    template_name = 'ingreso/nota_ingreso/nota.html'
    success_url = reverse_lazy('users_app:panel')

    def get_form_kwargs(self):
        kwargs = super(DepositSlipView, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user,
        })
        return kwargs

    def form_valid(self, form):
        # Recuperamos todos los datos del formulario
        serie = form.cleaned_data['serie']
        number = form.cleaned_data['number']
        origin = form.cleaned_data['origin']
        destination = form.cleaned_data['destination']
        count = form.cleaned_data['count']
        description = form.cleaned_data['description']
        total_amount = form.cleaned_data['total_amount']
        acuenta = form.cleaned_data['acuenta']

        sender_id = form.cleaned_data['sender_id']
        sender_name = form.cleaned_data['sender_name']
        sender_razonsocial = form.cleaned_data['sender_razonsocial']

        addr_id = form.cleaned_data['addr_id']
        addr_name = form.cleaned_data['addr_name']
        addr_razonsocial = form.cleaned_data['addr_razonsocial']

        user_created = self.request.user
        # Creamos cliente remitente   
        sender = ClientGetOrCreate(
            sender_id,
            sender_name,
            sender_razonsocial
        )
        # Creamos Cliete destinatario
        addressee = ClientGetOrCreate(
            addr_id,
            addr_name,
            addr_razonsocial
        )
        nota = DepositSlip(
            serie=serie,
            number=number,
            origin=origin,
            destination=description,
            sender=sender,
            addressee=addressee,
            date=datetime.now(),
            total_amount=total_amount
        )
        nota.save()

        print "----sender----"
        print sender.full_name
        print sender.ruc
        print sender.business_name
        print "----fin sender 000----"

        print "----addressee----"
        print addressee.full_name
        print addressee.ruc
        print addressee.business_name
        print "----fin addressee 000----"

        print "----------0-----------"
        print serie
        print number
        print "-------destinano y origen---------"
        print origin
        print destination
        print "-----------1-----------"
        print total_amount
        print acuenta
        print count
        print description
        print "------------2-----------"
        print sender_id
        print sender_name
        print sender_razonsocial
        print "-----------3-----------"
        print addr_id
        print addr_name
        print addr_razonsocial
        print "-------------4-----------"
        return super(DepositSlipView, self).form_valid(form)


class RegisterSlipView(FormView):
    form_class = NotaIngresoForm
    template_name = 'ingreso/slip.html'
    success_url = '.'

    #metodo para veriicar si hay algun detalle de producto
    def formulario_valido(self, detalles):
        resul = False
        for aux in detalles:
            if aux.is_valid():
                resul = True
        return resul

    #metodo que actualiza el datro dni o ruc de cliente
    def dni_ruc(self, cadena_id, cliente):
        #si la cadena contiene 11 caracteres gurdar en ruc
        if len(cadena_id) >= 11:
            cliente.ruc = cadena_id
            cliente.save()
        else:
            #caso contrario se guardara en dni
            cliente.dni = cadena_id
            cliente.save()

    def clinete_existe(self, cadena_id):
        if len(cadena_id) >= 11:
            #devolvemos uno si existe
            return Client.objects.filter(ruc=cadena_id)
        else:
            #devolvemos uno si el cliente existe
            return Client.objects.filter(dni=cadena_id)

    def get_context_data(self, **kwargs):
        context = super(RegisterSlipView, self).get_context_data(**kwargs)
        context['objetos'] = formset_factory(DetailForm, extra=2, max_num=3)
        return context

    def get_form_kwargs(self):
        kwargs = super(RegisterSlipView, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user,
        })
        return kwargs

    def form_valid(self, form):
        form_set = formset_factory(DetailForm, extra=2, max_num=3)
        ingreso_detalle = form_set(self.request.POST)
        if self.formulario_valido(ingreso_detalle):
            #verificamos si el cliente ya existe
            if self.clinete_existe(form.cleaned_data['sen_id']).count() > 0:
                #acuatalizmos los datos
                cliente_sen = self.clinete_existe(
                    form.cleaned_data['sen_id']
                )[0]
                cliente_sen.full_name = form.cleaned_data['sen_name']
                cliente_sen.business_name = form.cleaned_data['sen_razonsocial']
                cliente_sen.save()
                #mensaje de confirmacion
                print '=======Cliente Registrado======='
            else:
                #recuperamos datos de remitente
                cliente_sen = Client(
                    full_name=form.cleaned_data['sen_name'],
                    business_name=form.cleaned_data['sen_razonsocial'],
                )
                #guardamos nuevo remitente
                cliente_sen.save()
                #verificamos dni o ruc
                self.dni_ruc(form.cleaned_data['sen_id'], cliente_sen)
                #mensaje de confirmacion
                print '=======Cliente Registrado======='
            #verificamos si el destinatario ya existe
            if self.clinete_existe(form.cleaned_data['addr_id']).count() > 0:
                #actualizamos los dtos de cliente
                cliente_addr = self.clinete_existe(
                    form.cleaned_data['addr_id']
                )[0]
                cliente_addr.full_name = form.cleaned_data['addr_name']
                cliente_addr.business_name = form.cleaned_data['addr_razonsocial']
                cliente_addr.save()
                #mensaje de confirmacion
                print '=======Cliente Registrado======='
            else:
                #recuperamos datos de destinatario
                cliente_addr = Client(
                    full_name=form.cleaned_data['addr_name'],
                    business_name=form.cleaned_data['addr_razonsocial'],
                )
                #guardamos nuevo destinatario
                cliente_addr.save()
                #verificamos dni o ruc
                self.dni_ruc(form.cleaned_data['addr_id'], cliente_addr)
                #mensaje de confirmacion
                print '=======Cliente Registrado======='
            #recuperamos el origen
            origen = form.cleaned_data['origin']
            #recuperamos datos de NotaIngreso
            nota_ingreso = DepositSlip(
                serie=form.cleaned_data['serie'],
                number=form.cleaned_data['number'],
                origin=origen.branch,
                destination=form.cleaned_data['destination'],
                sender=cliente_sen,
                addressee=cliente_addr,
                date=datetime.now(),
                total_amount=form.cleaned_data['total'],
            )
            #guardamos nota de ingreso
            nota_ingreso.save()
            #mensaje de confirmacion
            print '=======Nota de ingreso Registrada======='
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
                sub_total = importe+igv
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
                user_created=self.request.user,
                user_modified=self.request.user,
            )
            #verificamos si la cuota cubre el monto total
            #guardamos cuota
            cuota.save()
            #mensaje de confirmacion
            print '=======Cuota Registrada======='
            #recuperamos datos para detalle de nota de ingreso (formset)
            ingreso_detalle = form_set(self.request.POST)
            for objeto in ingreso_detalle:
                if objeto.is_valid():
                    detalle = objeto.save(commit=False)
                    detalle.deposit_slip = nota_ingreso
                    detalle.user = self.request.user
                    detalle.save()
                    #mensaje de confirmacion
                    print '=======Detalle Registrado======='

        else:
            #Ingrese objetos correstos
            return HttpResponseRedirect('/errors/')

        return super(RegisterSlipView, self).form_valid(form)


class DeliverView(FormMixin, ListView):
    #model = Dues.objects.filter(deposit_slip__destination='1')
    context_object_name = 'paquetes'
    template_name = 'ingreso/entrega.html'

    def get_context_data(self, **kwargs):
        context = super(DeliverView, self).get_context_data(**kwargs)
        context['form'] = SearchForm
        return context

    def get_queryset(self):
        #recuperamos el valor por GET
        q = self.request.GET.get("serie")
        r = self.request.GET.get("number")
        s = self.request.GET.get("sender")
        t = self.request.GET.get("addressee")
        u = self.request.GET.get("date")
        #recuperamos el usuario o sucursal
        usuario = self.request.user
        sucursal = Profile.objects.filter(user=usuario)[0]
        #verificamos los campos recuperados por get
        if (q and r) or s or t or u:
            queryset = Dues.objects.buscar_ingreso(sucursal.branch, q, r, s, t)
        elif u:
            queryset = Dues.objects.buscar_by_fecha(sucursal, u)
        else:
            #tomamos la fecha actual
            fecha = timezone.now()
            queryset = Dues.objects.envios_no_entregados(
                sucursal.branch,
                fecha,
            )

        return queryset


class DetailDeliverView(FormMixin, DetailView):
    model = DepositSlip
    form_class = DetailDeliverForm
    template_name = 'ingreso/registro_entrega.html'
    success_url = reverse_lazy('ingreso_app:entrega-paquete')

    def get_context_data(self, **kwargs):
        context = super(DetailDeliverView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        objeto = self.object
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        #recupramos el objeto
        objeto = self.object
        #recuperamos el primer pago
        prime_pago = Dues.objects.get(deposit_slip=objeto).sub_total
        #calculamos el acuenta
        acuenta = objeto.total_amount - prime_pago
        #recuperamos el descuento
        descuento = form.cleaned_data['discount']
        #recuperamos el tipo de pago
        tipo_pago = form.cleaned_data['tipo']
        #calculamos el sub total
        sub_total = acuenta - descuento
        igv = 0
        #vrificamos el tipo de pago
        cadena_tipo = 'factura'
        if tipo_pago == cadena_tipo:
            igv = (sub_total/100) * 18
            sub_total = sub_total+igv
        #registramos el nuevo pago
        cuota = Dues(
            amount=acuenta,
            deposit_slip=objeto,
            date=datetime.now(),
            proof_type=tipo_pago,
            igv=igv,
            sub_total=sub_total,
            discount=descuento,
            user_created=self.request.user,
            user_modified=self.request.user,
        )
        objeto.commited = True
        objeto.save()
        cuota.save()
        #actualizamos el estado y registramos el descuento
        return super(DetailDeliverView, self).form_valid(form)
