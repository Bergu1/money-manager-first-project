from django import forms
from core.models import Account, AccountHistory

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['added_funds', 'source', 'date']
        widgets = {
            'added_funds': forms.NumberInput(attrs={'step': '0.01'}),
            'source': forms.TextInput(attrs={'type': 'text'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
