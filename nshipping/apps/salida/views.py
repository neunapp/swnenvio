from datetime import datetime
from braces.views import LoginRequiredMixin

from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import FormView, FormMixin
from django.utils import timezone
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect

from apps.users.models import User

from .models import Sesion, Expenditur
from .forms import ExpenditurForm, RealAmountForm, SearchForm
from .functions import list_expenditur, list_slip, total_anulate


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
            userstart=usuario,
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


class CountableCahs(LoginRequiredMixin, FormView):
    template_name = 'salida/reporte/cash.html'
    form_class = RealAmountForm
    success_url = reverse_lazy('users_app:login')
    login_url = reverse_lazy('users_app:login')

    def get_context_data(self, **kwargs):
        context = super(CountableCahs, self).get_context_data(**kwargs)
        #recuperamos la sesion
        user = self.request.user
        sesion = Sesion.objects.get(userstart=user, state=True)
        #enviamos la lista de de registros en la sesion
        lista = list_slip(sesion) + list_expenditur(sesion)
        context['lista'] = lista
        #enviamos el monto al que aciede los registros
        anulate, total = total_anulate(lista)
        context['anulate'] = anulate
        context['total'] = total
        return context

    def form_valid(self, form):
        amount = form.cleaned_data['amount']
        #usuario administrador
        userad = self.request.user
        #usuaro normal
        user_pk = self.kwargs.get('pk', 0)
        userno = User.objects.get(id=user_pk)
        #recuperamos la sesion del usuario
        sesion = Sesion.objects.get(userstart=userno, state=True)
        #actualizamos los datos en sesion
        sesion.state = False
        sesion.hourfinish = datetime.today()
        sesion.amount = amount
        sesion.userfinish = userad
        #guardamos los cambios
        sesion.save()
        return super(CountableCahs, self).form_valid(form)


class ListActives(LoginRequiredMixin, ListView):
    '''
    Busqueda sesiones activas.
    '''
    context_object_name = 'usuarios'
    template_name = 'salida/reporte/usuarios.html'
    login_url = reverse_lazy('users_app:login')

    def get_context_data(self, **kwargs):
        context = super(ListActives, self).get_context_data(**kwargs)
        context['form'] = SearchForm
        return context

    def get_queryset(self):
        #recuperamos el valor por GET
        q = self.request.GET.get("users", '')
        #devolvemos las sesiones activas del usuario
        queryset = Sesion.objects.filter(
            userstart__first_name__icontains=q,
            state=True,
        )
        return queryset
