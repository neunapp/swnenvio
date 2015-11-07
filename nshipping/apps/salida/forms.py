from django import forms

from .models import Cash, Expenditur


class ExpenditurForm(forms.ModelForm):
    class Meta:
        model = Expenditur
        fields = ('description', 'amount')
