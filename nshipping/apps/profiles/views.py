from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView

from .models import Profile
from .forms import ProfileForm
# Create your views here.


class ListProfile(ListView):
    context_object_name = 'perfiles'
    queryset = Profile.objects.all()
    template_name = 'profile/list.html'


class RegisterProfile(CreateView):
    template_name = 'profile/add.html'
    model = Profile
    success_url = '/'


class UpdateProfile(UpdateView):
    # matenimietno actualiza carro
    model = Profile
    template_name = 'profile/update.html'
    form_class = ProfileForm
    success_url = '/'
