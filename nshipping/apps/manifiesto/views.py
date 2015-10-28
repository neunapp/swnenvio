from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.views.generic.edit import FormMixin, FormView

from django.core.urlresolvers import reverse_lazy

from .models import Car, Driver, Manifest

from apps.ingreso.models import Dues

from .forms import CarForm, DriverForm, FilterForm


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


#proceso de registro de Manifiesto
class RegisterManifest(FormMixin, ListView):
    context_object_name = 'paquetes'
    template_name = 'manifiesto/manifest/register.html'

    def get_context_data(self, **kwargs):
        context = super(RegisterManifest, self).get_context_data(**kwargs)
        context['form'] = FilterForm
        return context

    def get_queryset(self):
        #recuperamos el valor recibido por get
        q = self.request.GET.get("destination")

        if q:
            queryset = Dues.objects.buscar_by_destino(q)
        else:
            queryset = Dues.objects.filter(deposit_slip__commited=False)

        return queryset

