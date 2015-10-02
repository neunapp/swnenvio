# -*- encoding: utf-8 -*-
from django import forms
from .models import User

from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    required_css_class = 'sr-only'

    username = forms.CharField(
        label='usuario',
        max_length='30',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su usuario',
                'autofocus': 'autofocus',
            }
        ),
    )
    password = forms.CharField(
        label='contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su password',
            }
        ),
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        print username, password

        if not authenticate(username=username, password=password):
            raise forms.ValidationError('usuario o contraseña es incorrecta ..!!')
        return self.cleaned_data
