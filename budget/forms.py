from django import forms
from .choices import INCOME_FREQUENCY_CHOICES

class ExpenseForm(forms.Form):
    date = forms.DateField()
    title = forms.CharField()
    amount = forms.IntegerField()
    category = forms.CharField()

class IncomeForm(forms.Form):
    date = forms.DateField()
    description = forms.CharField()
    amount = forms.IntegerField()
    source = forms.CharField()
    is_recurring = forms.BooleanField(required=False)
    recurring_frequency = forms.ChoiceField(choices=INCOME_FREQUENCY_CHOICES, required=False)