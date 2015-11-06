from datetime import datetime

from django.shortcuts import render
from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    ListView,
    TemplateView,
)
from django.views.generic.edit import FormMixin, SingleObjectMixin, FormView
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect

from apps.ingreso.models import Dues, Branch, DepositSlip
from apps.profiles.models import Profile

from .models import Car, Driver, Manifest

from .forms import CarForm, DriverForm, FilterForm, RegisterManifestForm


#mantenimiento para tabla Car
class ListCarView(ListView):
    context_object_name = 'carros'
    queryset = Car.objects.all()
    template_name = 'manifiesto/car/list.html'


class RegisterCarView(CreateView):
#mantenimiento agregar Carro
    form_class = CarForm
    template_name = 'manifiesto/car/add.html'
    success_url = reverse_lazy('manifiesto_app:agregar-carro')


class UpdateCarView(UpdateView):
    #matenimietno actualiza carro
    model = Car
    template_name = 'manifiesto/car/update.html'
    form_class = CarForm
    success_url = reverse_lazy('manifiesto_app:listar-carro')


#mantenimeinto para tabla Conductor
class ListDriverView(ListView):
    context_object_name = 'conductores'
    queryset = Driver.objects.all()
    template_name = 'manifiesto/driver/list.html'


class RegisterDriverView(CreateView):
    #mantenimiento registrar conductor
    template_name = 'manifiesto/driver/add.html'
    form_class = DriverForm
    success_url = reverse_lazy('manifiesto_app:listar-conductor')


class UpdateDriverView(UpdateView):
    #mantenimient actualizar conductor
    template_name = 'manifiesto/driver/update.html'
    model = Driver
    form_class = DriverForm
    success_url = reverse_lazy('manifiesto_app:listar-conductor')


# #proceso para registrar manifiesto
class RegisterManifestView(FormView):
    form_class = RegisterManifestForm
    template_name = 'manifiesto/manifest/register.html'

    def get_form_kwargs(self):
        kwargs = super(RegisterManifestView, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user,
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(RegisterManifestView, self).get_context_data(**kwargs)
        usuario = self.request.user
        profile = Profile.objects.filter(user=usuario)[0]
        context['slips'] = DepositSlip.objects.filter(
            destination=profile.branch,
            commited=False,
        )
        return context

    def form_valid(self, form):
        #recperamos la sucursal
        usuario = self.request.user
        sucursal = Profile.objects.get(user=usuario).branch
        #recuperamos las notas de ingreso seleccionadas
        deposit = form.cleaned_data['deposit_slip']
        for slip in deposit:
            #actualizamos la DS como enviado
            nota_ingreso = slip
            nota_ingreso.output = True
            nota_ingreso.save()
        #registramos el manifiesto del envio
        manifiesto = form.save()
        manifiesto.destination = sucursal
        manifiesto.user = self.request.user
        manifiesto.date = datetime.now()
        manifiesto.save()
        print '======manifiesto GUARDADO====='
        print manifiesto.pk
        #mostramos la lista de reportes a imprimir por sucursal
        return HttpResponseRedirect(
            reverse(
                'manifiesto_app:reporte-manifiesto',
                kwargs={'pk': manifiesto.pk},
            )
        )


class ReportManifest(DetailView):
    model = Manifest
    template_name = 'manifiesto/manifest/report.html'

    def get_context_data(self, **kwargs):
        context = super(ReportManifest, self).get_context_data(**kwargs)
        #recuperamos le manifiesto enviado por url
        manifisto = self.object
        #recuperamos las notas de ingreso de manifiesto
        #slips=lista de notas de ingreso
        slips = manifisto.deposit_slip.all()
        #lbranch = lista de sucursales distintas de slips
        lbranch = []
        aux = ""
        for s in slips:
            if s.destination.name != aux:
                aux = s.destination.name
                #agregamos la sucursal
                lbranch.append(s.destination)

        #asignamos lbranch como contexto
        context['sucursales'] = lbranch
        return context


#clase para mostrar los notas de ingreso de una sucursal y un manifiesto
class ReportDetailM(TemplateView):
    template_name = 'manifiesto/manifest/detalle-reporte.html'

    def get_context_data(self, **kwargs):
        context = super(ReportDetailM, self).get_context_data(**kwargs)
        #recuperamos manifest y branch de url
        manifiesto = kwargs.get('pk', 0)
        sucursal = kwargs.get('br', 0)
        #recuperamos objetos manifes y branch
        manifest = Manifest.objects.get(pk=manifiesto)
        branch = Branch.objects.get(pk=sucursal)
        #listamos deposit_slip con branch y manifest
        #ldeposit = lita de Depostslip de mismo destino
        ldeposit = []
        for ds in manifest.deposit_slip.all():
            if ds.destination == branch:
                #agregamos el dpositslip
                ldeposit.append(ds)
        #devolvemos la lista como contexto
        context['slips'] = ldeposit
        return context
