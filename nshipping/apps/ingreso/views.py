# -*- encoding: utf-8 -*-
from django.views.generic import TemplateView, DetailView, UpdateView
from django.views.generic.edit import CreateView, FormView, FormMixin
from django.views.generic.list import ListView

from django.core.urlresolvers import reverse_lazy

# local.
from .functions import ClientGetOrCreate
from .models import Branch, Client, Dues, DepositSlip
from .forms import (
    NotaIngresoForm,
    ClientForm,
    SearchForm,
    DetailDeliverForm,
    BranchForm
)

from apps.profiles.models import Profile


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
        voucher = form.cleaned_data['voucher']
        guide = form.cleaned_data['guide']
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

        depositslip = DepositSlip(
            serie=serie,
            number=number,
            origin=origin,
            destination=destination,
            sender=sender,
            addressee=addressee,
            voucher=voucher,
            guide=guide,
            total_amount=total_amount,
            count=count,
            description=description,
            user_created=user_created
        )
        depositslip.save()

        dues = Dues(
            depositslip=depositslip,
            amount=acuenta,
            user_created=user_created
        )
        dues.save()

        return super(DepositSlipView, self).form_valid(form)


class DeliverView(FormMixin, ListView):
    #model = Dues.objects.filter(deposit_slip__destination='1')
    context_object_name = 'paquetes'
    template_name = 'ingreso/entrega/entrega.html'

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
        user = self.request.user
        user_profile = Profile.objects.get(user=user)
        # funcion lamda para verificar si es nome
        xstr = lambda s: s or ''

        q = xstr(q)
        r = xstr(r)
        s = xstr(s)
        t = xstr(t)
        u = xstr(u)

        queryset = Dues.objects.search(q, r, s, t, user_profile.branch , u)
        return queryset
