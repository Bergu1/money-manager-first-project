from django.shortcuts import render, redirect
from .forms import AccountForm
from django.contrib.auth.decorators import login_required
from django.db.models.functions import ExtractMonth, ExtractYear
from core.models import AccountHistory

@login_required
def account(request):
    account = request.user.account

    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)  
        if form.is_valid():
            added_funds = form.cleaned_data['added_funds']
            if added_funds > 0:
                account.update_balance(added_funds, "add")
                account.added_funds = 0
            return redirect('account')
        else:
            print(form.errors)
    else:
        form = AccountForm(instance=account)

    return render(request, 'account/account.html', {'form': form, 'total_balance': account.total_balance})



@login_required
def show_deposit(request):
    deposits = None
    if request.method == 'POST':
        month = int(request.POST.get('month'))
        year = int(request.POST.get('year'))
        if month and year:
            deposits = AccountHistory.objects.annotate(
                month=ExtractMonth('date'),
                year=ExtractYear('date')
            ).filter(
                account=request.user.account,
                year=year,
                month=month,
                added_funds__gt=0  
            )

    return render(request, 'account/show_deposit.html', {'deposits': deposits})