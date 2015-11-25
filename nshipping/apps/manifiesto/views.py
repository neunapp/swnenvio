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

from .models import Car, Driver, Manifest, SubContract
from .forms import (
    CarForm,
    DriverForm,
    FilterForm,
    ManifestForm,
    RemissionForm,
    ThirdManifestForm,
    ReceptionForm,
)


#mantenimiento para tabla Car
class ListCarView(ListView):
    context_object_name = 'carros'
    queryset = Car.objects.filter(canceled=False)
    template_name = 'manifiesto/car/list.html'


class RegisterCarView(CreateView):
#mantenimiento agregar Carro
    form_class = CarForm
    template_name = 'manifiesto/car/add.html'
    success_url = reverse_lazy('manifiesto_app:listar-carro')


class UpdateCarView(UpdateView):
    #matenimietno actualiza carro
    model = Car
    template_name = 'manifiesto/car/update.html'
    form_class = CarForm
    success_url = reverse_lazy('manifiesto_app:listar-carro')


class DeleteCarView(DetailView):
    template_name = 'manifiesto/car/delete.html'
    model = Car

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        #recuperamos el objeto y actualizamos a anulado
        car = self.object
        #actualizamos y guardamos el valor
        car.canceled = True
        car.save()
        print 'print objeto acutalizado'
        return HttpResponseRedirect(
            reverse(
                'manifiesto_app:listar-carro'
            )
        )


class DetailCarView(DetailView):
    template_name = 'manifiesto/car/detail.html'
    model = Car


#mantenimeinto para tabla Conductor
class ListDriverView(ListView):
    context_object_name = 'conductores'
    queryset = Driver.objects.filter(canceled=False)
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


class DeleteDriverView(DetailView):
    #metodo para inhabilitar un conductor
    template_name = 'manifiesto/driver/delete.html'
    model = Driver

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        #recuperamos el objeto y actualizamos a anulado
        driver = self.object
        #actualizamos y guardamos el valor
        driver.canceled = True
        driver.save()
        print 'print objeto acutalizado'
        return HttpResponseRedirect(
            reverse(
                'manifiesto_app:listar-conductor'
            )
        )


class DetailDriverView(DetailView):
    #metodo para vizualizar los datos de conductor
    template_name = 'manifiesto/driver/detail.html'
    model = Driver


#mantinimietos de manifeisto
class ManifestList(ListView):
    template_name = 'manifiesto/manifest/list.html'
    context_object_name = 'manifests'
    queryset = Manifest.objects.filter(
        canceled=False,
        reception=False,
    )


# #proceso para registrar manifiesto
class ManifestView(FormView):
    template_name = 'manifiesto/manifest/add.html'
    form_class = ManifestForm
    success_url = reverse_lazy('manifiesto_app:listar-manifiesto')

    def form_valid(self, form):
        #recuperamos los datos para manifest
        driver = form.cleaned_data['driver']
        car = form.cleaned_data['car']
        destination = form.cleaned_data['destination']
        origin = form.cleaned_data['origin']
        date_shipping = form.cleaned_data['date_shipping']
        user_created = self.request.user
        user_modified = self.request.user
        #guardamos el manifiesto
        manifest = Manifest(
            driver=driver,
            car=car,
            destination=destination,
            origin=origin,
            user_created=user_created,
            user_modified=user_modified,
            date_shipping=date_shipping,
            state=False,
        )
        manifest.save()
        return super(ManifestView, self).form_valid(form)


#metodo para modificar un manifiesto
class UpdateManifest(UpdateView):
    template_name = 'manifiesto/manifest/update.html'
    model = Manifest
    form_class = ManifestForm
    success_url = reverse_lazy('manifiesto_app:listar-manifiesto')


class AnulateManifestView(DetailView):
    #metodo para anular un manifiesto
    template_name = 'manifiesto/manifest/delete.html'
    model = Manifest

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        #recuperamos el objeto y actualizamos a anulado
        manifest = self.object
        #actualizamos y guardamos el valor
        manifest.canceled = True
        manifest.save()
        print 'print objeto acutalizado'
        return HttpResponseRedirect(
            reverse(
                'manifiesto_app:listar-manifiesto'
            )
        )


class FullManifestView(DetailView):
    #metodo para actualizar estado de manifiesto a lleno
    template_name = 'manifiesto/manifest/full.html'
    model = Manifest

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        #recuperamos el objeto y actualizamos a anulado
        manifest = self.object
        #actualizamos los productos a enviado
        for deposit_slip in manifest.deposit_slip.all():
            deposit_slip.state = '1'
            #guardamos el deposit slip
            deposit_slip.save()
            print deposit_slip.state
        #actualizamos y guardamos el valor
        manifest.state = True
        manifest.save()
        return HttpResponseRedirect(
            reverse(
                'manifiesto_app:reporte-manifiesto',
                kwargs={'pk': manifest.pk},
            )
        )


class Complete_Manifest(DetailView):
    #metodo para actualizar estado de manifest a Recepcionado
    template_name = 'manifiesto/manifest/complete.html'
    model = Manifest

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        #recuperamos el objeto y actualizamos a anulado
        manifest = self.object
        #actualizamos el manifiesto a recepcionado
        manifest.reception = True
        manifest.save()
        return HttpResponseRedirect(
            reverse(
                'manifiesto_app:reporte-manifiesto',
                kwargs={'pk': manifest.pk},
            )
        )


class DetailManifestView(DetailView):
    #metodo para vizualizar los datos de conductor
    template_name = 'manifiesto/manifest/detail.html'
    model = Manifest


#proceso para registrar una guia de remision
class RemissionView(FormMixin, DetailView):
    '''vista para registrar las notas de ingreso
        en un manifiesto '''
    model = DepositSlip
    form_class = RemissionForm
    template_name = 'manifiesto/remision/add.html'

    def get_success_url(self):
        return reverse_lazy('ingreso_app:nota-ingreso')

    def get_form_kwargs(self):
        kwargs = super(RemissionView, self).get_form_kwargs()
        print '=======entro a los kwargs====='
        kwargs.update({
            'pk': self.kwargs.get('pk', 0),
            'user': self.request.user,
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(RemissionView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        #recuperamos el manifiesto de formulario
        manifest = form.cleaned_data['manifest']
        #agregamos la nota de ingreso al manifest
        manifest.deposit_slip.add(self.object)
        #guardamos le Manifest
        manifest.save()
        print '======nota de ingreso agreagda======'
        return super(RemissionView, self).form_valid(form)


#manifieto con cotrata a terceros
class ThirdManifestView(FormView):
    template_name = 'manifiesto/manifest/subcontrata.html'
    form_class = ThirdManifestForm
    success_url = reverse_lazy('manifiesto_app:listar-manifiesto')

    def form_valid(self, form):
        #recuperamos los datos para manifest
        driver = form.cleaned_data['driver']
        car = form.cleaned_data['car']
        destination = form.cleaned_data['destination']
        origin = form.cleaned_data['origin']
        date_shipping = form.cleaned_data['date_shipping']
        user_created = self.request.user
        user_modified = self.request.user
        #datos para la tabla observaciones
        full_name = form.cleaned_data['full_name']
        ruc = form.cleaned_data['ruc']
        observations = form.cleaned_data['observations']
        #guardamos el manifiesto
        manifest = Manifest(
            driver=driver,
            car=car,
            destination=destination,
            origin=origin,
            user_created=user_created,
            user_modified=user_modified,
            date_shipping=date_shipping,
            state=False,
        )
        manifest.save()
        '===========manifiesto guardado============'
        #se registra los datos en subcontrac
        subcontrac = SubContract(
            manifest=manifest,
            full_name=full_name,
            ruc=ruc,
            observation=observations,
        )
        #guradamos datos de sub contrata
        subcontrac.save()
        '==============sub contrata guardad============'
        return super(ThirdManifestView, self).form_valid(form)


#proceso para listar destinos de un manifiesto
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


#proceso para mostrar los notas de ingreso de una sucursal y un manifiesto
class ReportDetailManifest(TemplateView):
    template_name = 'manifiesto/manifest/detalle-reporte.html'

    def get_context_data(self, **kwargs):
        context = super(ReportDetailManifest, self).get_context_data(**kwargs)
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


#lista de manifiestos no recepcionadoss
class Manifest_no_Reception(ListView):
    context_object_name = 'manifests'
    queryset = Manifest.objects.filter(reception=False)
    template_name = 'manifiesto/reception/list.html'


#lista de notas de ingreso a recpcionar
class Slip_Reception(FormMixin, DetailView):
    model = Manifest
    form_class = ReceptionForm
    template_name = 'manifiesto/reception/recepcion.html'

    def get_success_url(self):
        return reverse_lazy('ingreso_app:nota-ingreso')

    def get_form_kwargs(self):
        kwargs = super(Slip_Reception, self).get_form_kwargs()
        print '=======entro a los kwargs====='
        kwargs.update({
            'pk': self.kwargs.get('pk', 0),
            'user': self.request.user,
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(Slip_Reception, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        #recuperamos el manifiesto de formulario
        deposit_slip = form.cleaned_data['deposit_slip']
        for slip in deposit_slip:
            slip.state = '2'
            slip.save()
        print '======nota de ingreso actualizada======'
        return super(Slip_Reception, self).form_valid(form)
