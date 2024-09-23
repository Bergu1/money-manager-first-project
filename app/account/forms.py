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

    def clean_added_funds(self):
        added_funds = self.cleaned_data.get('added_funds')
        if added_funds < 0:
            raise forms.ValidationError("Ensure this value is greater than or equal to 0.")
        return added_funds
