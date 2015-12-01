from braces.views import LoginRequiredMixin

from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import FormView, FormMixin
from django.utils import timezone
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect

from apps.users.models import User

from .models import Sesion, Expenditur
from .forms import ExpenditurForm


#clase para listar los ingresos
class ListExpenditur(LoginRequiredMixin, ListView):
    context_object_name = 'egresos'
    queryset = Expenditur.objects.filter(canceled=False)
    template_name = 'salida/egresos/list.html'
    login_url = reverse_lazy('users_app:login')


#calse para registrar un igreso
class RegisterExpenditur(LoginRequiredMixin, FormView):
    form_class = ExpenditurForm
    template_name = 'salida/egresos/add.html'
    success_url = reverse_lazy('salida_app:listar-egreso')
    login_url = reverse_lazy('users_app:login')

    def form_valid(self, form):
        #recuperamos usuaro activo
        usuario = self.request.user
        #recuperamos la sesion del usuario
        sesion = Sesion.objects.get(
            user_created=usuario,
            state=True,
        )
        #recuperamos descripcion y monto del form:class
        importe = form.cleaned_data['amount']
        descripcion = form.cleaned_data['description']
        #creamos el objeto Expedition
        egresos = Expenditur(
            description=descripcion,
            amount=importe,
            user_created=usuario,
            user_modified=usuario,
            sesion=sesion,
        )
        #guardamos objeto egresos
        egresos.save()
        print 'egresos registrados'

        return super(RegisterExpenditur, self).form_valid(form)


class DetailExpenditur(LoginRequiredMixin, DetailView):
    #metodo para vizualizar los datos de conductor
    template_name = 'salida/egresos/detail.html'
    model = Expenditur
    login_url = reverse_lazy('users_app:login')


class AnulateExpenditur(LoginRequiredMixin, FormMixin, DetailView):
    #metodo para inhabilitar un conductor
    template_name = 'salida/egresos/update.html'
    model = Expenditur
    login_url = reverse_lazy('users_app:login')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        #recuperamos el objeto y actualizamos a anulado
        expenditur = self.object
        #actualizamos y guardamos el valor
        expenditur.canceled = True
        expenditur.user_modified = self.request.user
        expenditur.save()
        print 'print objeto acutalizado'
        return HttpResponseRedirect(
            reverse(
                'salida_app:listar-egreso'
            )
        )
