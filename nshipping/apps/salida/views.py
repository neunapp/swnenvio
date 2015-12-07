from datetime import datetime
from braces.views import LoginRequiredMixin

from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import FormView, FormMixin
from django.utils import timezone
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect

from apps.users.models import User
from apps.ingreso.models import Dues

from .models import Sesion, Expenditur
from .forms import ExpenditurForm, RealAmountForm, SearchForm, FilterForm
from .functions import list_expenditur, list_slip, resul_proces


#clase para listar los ingresos
class ListExpenditur(LoginRequiredMixin, ListView):
    context_object_name = 'egresos'
    template_name = 'salida/egresos/list.html'
    login_url = reverse_lazy('users_app:login')

    def get_queryset(self):
        # calculamos los resultados
        user_pk = self.request.user
        sesion = Sesion.objects.get(userstart=user_pk, state=True)
        #realizamos las consultas
        queryset = Expenditur.objects.filter(
            canceled=False,
            sesion=sesion
        )
        return queryset


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


class CountableCahs(LoginRequiredMixin, FormMixin, ListView):
    context_object_name = 'lista'
    template_name = 'salida/reporte/cash.html'
    form_class = RealAmountForm
    success_url = reverse_lazy('users_app:logout')
    login_url = reverse_lazy('users_app:login')

    def get_context_data(self, **kwargs):
        context = super(CountableCahs, self).get_context_data(**kwargs)
        #recuperamos la sesion
        user_pk = self.kwargs.get('pk', 0)
        userno = User.objects.get(id=user_pk)
        sesion = Sesion.objects.get(userstart=userno, state=True)
        # recuperamos las notas de ingreso creadas y entregdas
        slip_sesion = Dues.objects.filter(depositslip__sesion=sesion)
        deliver_sesion = Dues.objects.filter(sesion=sesion)
        expenditur_sesion = Expenditur.objects.filter(sesion=sesion)
        # enviamos resultados al contexto
        context['resultados'] = resul_proces(
            slip_sesion,
            deliver_sesion,
            expenditur_sesion
        )
        context['tipo'] = FilterForm
        context['form'] = self.get_form()
        return context

    def get_queryset(self):
        # calculamos los resultados
        user_pk = self.kwargs.get('pk', 0)
        userno = User.objects.get(id=user_pk)
        sesion = Sesion.objects.get(userstart=userno, state=True)
        #realizamos las consultas
        slip_sesion = Dues.objects.filter(depositslip__sesion=sesion)
        deliver_sesion = Dues.objects.filter(sesion=sesion)
        expenditur_sesion = Expenditur.objects.filter(sesion=sesion)
        #procesamos las listas
        a, b, c, d = list_slip(slip_sesion)
        q, r, s, t = list_slip(deliver_sesion)
        #recupermos los egresos
        w, x, y, z = list_expenditur(expenditur_sesion)
        # recuperamos el valor por GET
        tipo = self.request.GET.get("tipo", '')
        if tipo == '1':
            queryset = b + r + x
        else:
            queryset = a + q + w
        return queryset

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

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
