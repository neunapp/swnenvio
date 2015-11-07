from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import FormView, FormMixin
from django.utils import timezone

from apps.users.models import User

from .models import Cash, Expenditur
from .forms import ExpenditurForm


#clase para listar los ingresos
class ListExpenditur(TemplateView):
    template_name = 'salida/egresos/list.html'

    def get_context_data(self, **kwargs):
        context = super(ListExpenditur, self).get_context_data(**kwargs)
        context['egresos'] = Expenditur.objects.filter(anulate=False)
        return context


#calse para registrar un igreso
class RegisterExpenditur(FormView):
    form_class = ExpenditurForm
    template_name = 'salida/egresos/add.html'
    success_url = '.'

    def form_valid(self, form):
        #recuperamos usuaro activo
        usuario = self.request.user
        #recupermaos fecha
        fecha = timezone.now()
        #recuperamos descripcion y monto del form:class
        importe = form.cleaned_data['amount']
        descripcion = form.cleaned_data['description']
        #creamos el objeto Expedition
        egresos = Expenditur(
            description=descripcion,
            amount=importe,
            user=usuario,
            date=fecha,
            user_created=usuario,
            user_modified=usuario,
        )
        #guardamos objeto egresos
        egresos.save()
        print 'egresos registrados'

        return super(RegisterExpenditur, self).form_valid(form)


class AnulateExpenditur(FormMixin, DetailView):
    model = Expenditur
    template_name = 'salida/egresos/update.html'
    succes_url = '/'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        egreso = self.object
        egreso.user_modified = self.request.user
        egreso.anulate = True
        egreso.save()
        print '========boleta anulada============'
        return render(request, 'ingreso/nota_ingreso/nota.html')
