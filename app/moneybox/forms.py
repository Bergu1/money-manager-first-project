from django import forms
from core.models import SavingsGoal

class SavingsGoalForm(forms.ModelForm):
    class Meta:
        model = SavingsGoal
        fields = ['target_amount']


class TransferToSavingsForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)


class CashOutForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

