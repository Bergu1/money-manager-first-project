from django import forms
from core.models import DailyBuy, Bills, Random_expenses


class DailyBuyForm(forms.ModelForm):
    class Meta:
        model = DailyBuy
        fields = ['day', 'date', 'shop', 'product', 'price']
        widgets = {
            'day': forms.Select(choices=DailyBuy.DAYS_OF_WEEK),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'shop': forms.TextInput(attrs={'type': 'text'}),
            'product': forms.TextInput(attrs={'type': 'text'}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }


class BillsForm(forms.ModelForm):
    class Meta:
        model = Bills
        fields = ['date', 'fee', 'price']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'fee': forms.TextInput(attrs={'type': 'text'}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }


class RandomExpensesForm(forms.ModelForm):
    class Meta:
        model = Random_expenses
        fields = ['date', 'for_what', 'price']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'for_what': forms.TextInput(attrs={'type': 'text'}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }