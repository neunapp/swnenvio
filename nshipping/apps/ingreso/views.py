# -*- encoding: utf-8 -*-
from braces.views import LoginRequiredMixin

from django.views.generic import DetailView, UpdateView
from django.views.generic.edit import CreateView, FormView, FormMixin
from django.views.generic.list import ListView
from django.contrib.messages.views import SuccessMessageMixin

from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect

# local.
from .functions import ClientGetOrCreate
from .models import Branch, Dues, DepositSlip
from apps.profiles.models import Profile
from apps.salida.models import Expenditur, Sesion
from .forms import (
    NotaIngresoForm,
    SearchForm,
    DetailDeliverForm,
    BranchForm
)


# Mantenimiento de sucursales
class ListBranchView(LoginRequiredMixin, ListView):
    context_object_name = 'sucursales'
    queryset = Branch.objects.filter(canceled=False)
    template_name = 'ingreso/sucursal/list.html'
    login_url = reverse_lazy('users_app:login')

    def get_context_data(self, **kwargs):
        context = super(ListBranchView, self).get_context_data(**kwargs)
        context['cantidad'] = self.object_list.count
        return context


class RegisterBranchView(LoginRequiredMixin, CreateView):
    # mantenimiento registrar sucursal
    template_name = 'ingreso/sucursal/add.html'
    form_class = BranchForm
    success_url = reverse_lazy('ingreso_app:listar-branch')
    login_url = reverse_lazy('users_app:login')


class UpdateBranchView(LoginRequiredMixin, UpdateView):
    model = Branch
    template_name = 'ingreso/sucursal/update.html'
    form_class = BranchForm
    success_url = reverse_lazy('ingreso_app:listar-branch')
    login_url = reverse_lazy('users_app:login')


class DeleteBranchView(LoginRequiredMixin, DetailView):
    # metodo para inhabilitar un sucursal
    template_name = 'ingreso/sucursal/delete.html'
    model = Branch
    login_url = reverse_lazy('users_app:login')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # recuperamos el objeto y actualizamos a anulado
        branch = self.object
        # actualizamos y guardamos el valor
        branch.canceled = True
        branch.save()
        print 'print objeto acutalizado'
        return HttpResponseRedirect(
            reverse(
                'ingreso_app:listar-branch'
            )
        )


class DetailBranchView(LoginRequiredMixin, DetailView):
    # metodo para vizualizar los datos de sucursal
    template_name = 'ingreso/sucursal/detail.html'
    model = Branch
    login_url = reverse_lazy('users_app:login')


class DepositSlipView(LoginRequiredMixin, FormView):
    '''
    vista para en registro de la nota de ingreso
    '''
    form_class = NotaIngresoForm
    template_name = 'ingreso/nota_ingreso/nota.html'
    success_url = reverse_lazy('users_app:panel')
    login_url = reverse_lazy('users_app:login')

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
        # recuperamos la sesion del usuario
        sesion = Sesion.objects.get(
            userstart=user_created,
            state=True,
        )
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
            user_created=user_created,
            sesion=sesion,
        )
        depositslip.save()

        dues = Dues(
            depositslip=depositslip,
            amount=acuenta,
            user_created=user_created,
            sesion=sesion
        )
        dues.save()

        return HttpResponseRedirect(
            reverse(
                'manifiesto_app:register-remission',
                kwargs={'pk': depositslip.pk},
            )
        )


class DeliverView(LoginRequiredMixin, ListView):
    '''
    Busqueda de paquetes o envios llegados
    a la sucursal.
    '''
    context_object_name = 'paquetes'
    template_name = 'ingreso/entrega/entrega.html'
    login_url = reverse_lazy('users_app:login')

    def get_context_data(self, **kwargs):
        context = super(DeliverView, self).get_context_data(**kwargs)
        context['form'] = SearchForm
        return context

    def get_queryset(self):
        # recuperamos el valor por GET
        q = self.request.GET.get("serie", '')
        r = self.request.GET.get("number", '')
        s = self.request.GET.get("sender", '')
        t = self.request.GET.get("addressee", '')
        u = self.request.GET.get("date", '')
        # recuperamos el usuario
        user = self.request.user
        # Recuperamos la sucursal del usuario
        user_profile = Profile.objects.get(user=user)

        queryset = Dues.objects.search(q, r, s, t, user_profile.branch, u)
        return queryset


class DetailDeliverView(LoginRequiredMixin, SuccessMessageMixin, FormMixin, DetailView):
    '''
    Detalle del envio y registro de la cuota
    si hay descuento se regitra en la tabla salida.
    '''
    model = DepositSlip
    form_class = DetailDeliverForm
    template_name = 'ingreso/entrega/entrega_detalle.html'
    success_url = reverse_lazy('users_app:panel')
    success_message = "El paquete con nota de ingreso %(serie)s - %(number)s \
                        fue entregado correctamente."
    login_url = reverse_lazy('users_app:login')

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            serie=self.object.serie,
            number=self.object.number,
        )

    def get_context_data(self, **kwargs):
        context = super(DetailDeliverView, self).get_context_data(**kwargs)
        dues = Dues.objects.get(pk=self.object.pk, canceled=False)
        porcobrar = self.object.total_amount - dues.amount
        context['form'] = self.get_form()
        context['acuenta'] = dues.amount
        context['porcobrar'] = porcobrar
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # recupramos el objeto
        depositslip = self.object
        depositslip.state = '3'
        depositslip.save()

        descuento = form.cleaned_data['discount']
        user = self.request.user
        # Recuperamos el monto de la primera cuota.
        dues1 = Dues.objects.get(pk=self.object.pk, canceled=False)
        # restamos el de monto total y el monto de la primera cuota.
        amount = self.object.total_amount - dues1.amount
        # Creamos y guardamso la segunda cuota.
        dues2 = Dues(
            depositslip=depositslip,
            amount=amount,
            user_created=user
        )
        dues2.save()
        # Verificamos si el descuento es mayor a cero
        # para guardalo como salida.
        if descuento > 0:
            msj = 'descuento de la nota de ingreso %s %s' \
                % (depositslip.serie, depositslip.number)

            expenditur = Expenditur(
                description=msj,
                amount=descuento,
                user_created=user,
                user_modified=user,
            )
            expenditur.save()

        return super(DetailDeliverView, self).form_valid(form)
