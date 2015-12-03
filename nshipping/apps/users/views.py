from datetime import datetime

from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout

from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect

from apps.salida.models import Sesion
from apps.profiles.models import Profile


class LogIn(FormView):
    form_class = LoginForm
    template_name = "users/login.html"
    success_url = reverse_lazy('users_app:panel')

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user is not None:
            if user.is_active:
                login(self.request, user)
                #recuperamos la sesion
                s = Sesion.objects.filter(
                    userstart=user,
                    state=True,
                )
                #si la sesion no existe la creamos
                if s.count() < 1:
                    #recuperamos la sucursal del usuario
                    perfil = Profile.objects.filter(user=user)
                    #si exste la sucursal no es admin
                    if perfil.count() > 0:
                        sesion = Sesion(
                            userstart=user,
                            state=True,
                            branch=perfil[0].branch,
                            capitel=0.00,
                            hourstart=datetime.today(),
                            amount=0.00,
                        )
                        sesion.save()
                        print 'Sesion usuario normal'
                    else:
                        sesion = Sesion(
                            userstart=user,
                            state=True,
                            capitel=0.00,
                            hourstart=datetime.today(),
                            amount=0.00,
                        )
                        sesion.save()
                        print 'sesion usuario administrador'

        return super(LogIn, self).form_valid(form)


class LogAdmin(FormView):
    form_class = LoginForm
    template_name = "users/login.html"
    success_url = '/'

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return HttpResponseRedirect(
                    reverse(
                        'salida_app:reporte-salidas',
                        kwargs={'pk': self.kwargs.get('pk', 0)},
                    )
                )


def LogOut(request):
    logout(request)
    return redirect('/')


class PanelView(TemplateView):
    template_name = "users/panel/panel.html"


class Panel2View(TemplateView):
    template_name = "ingreso/entrega/entrega.html"


class Panel3View(TemplateView):
    template_name = "ingreso/entrega/entrega_detalle.html"
