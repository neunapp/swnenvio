# -*- encoding: utf-8 -*-

from django import forms

from .models import Cash, Expenditur


class ExpenditurForm(forms.ModelForm):
    class Meta:
        model = Expenditur
        fields = ('description', 'amount')

        widgets = {
            'amount': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control input-detail',
                    'placeholder': 'Ingrese una descripción',
                    'rows': '4'
                }
            ),
        }

    def clean_amount(self):
        monto = self.cleaned_data['amount']
        if monto < 1:
            raise forms.ValidationError("Ingrese un numero de telefono valido")
        else:
            return monto
