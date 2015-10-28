from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.views.generic.edit import FormMixin, SingleObjectMixin, FormView

from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from datetime import datetime

from .models import Car, Driver, Manifest

from apps.ingreso.models import Dues, Branch, DepositSlip

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


class DeleteCarView(DeleteView):
    #mantenimiento eliminar carro
    template_name = 'manifiesto/car/delete.html'
    model = Car
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


class DeleteDriverView(DeleteView):
    #mantenimiento eliminar conductor
    template_name = 'manifiesto/driver/delete.html'
    model = Driver
    success_url = reverse_lazy('manifiesto_app:listar-conductor')



# #proceso para registrar manifiesto
class RegisterManifestView(SingleObjectMixin, FormView):
    form_class = RegisterManifestForm
    template_name = 'manifiesto/manifest/register.html'
    success_url = '.'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Branch.objects.all())
        return super(RegisterManifestView, self).get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(RegisterManifestView,self).get_form_kwargs()
        kwargs.update({
            'pk': self.kwargs.get('pk',0),
                      })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(RegisterManifestView, self).get_context_data(**kwargs)
        context['slips'] = DepositSlip.objects.filter(destination=self.object,commited=False)
        return context


    def form_valid(self, form):
        #recuperamos las notas de ingreso seleccionadas
        if form.is_valid():
            #actualizamos el dposit_slip
            deposit = forms.cleaned_data['deposit_slip']
            for slip in deposit:
                nota_ingreso = slip
                nota_ingreso.output = True
                nota_ingreso.save()

            manifiesto = form.save()
            manifiesto.user = self.request.user
            manifiesto.date = datetime.now()
            manifiesto.save()

        return super(RegisterManifestView, self).form_valid(form)