from django.shortcuts import render, redirect
from .forms import AccountForm
from django.contrib.auth.decorators import login_required
from django.db.models.functions import ExtractMonth, ExtractYear
from core.models import AccountHistory
from django.contrib import messages

@login_required
def account(request):
    account = request.user.account
    currency = request.user.currency
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)  
        if form.is_valid():
            added_funds = form.cleaned_data['added_funds']
            if added_funds > 0:
                account.added_funds = request.user.convert_price_write(added_funds, currency)
                account.update_balance(account.added_funds, "add")
                account.added_funds = 0
                messages.success(request, 'Added successfully!')
            return redirect('account')
        else:
            print(form.errors)
    else:
        form = AccountForm(instance=account)
    account.total_balance_display = round(request.user.convert_price(account.total_balance, currency), 2)
    return render(request, 'account/account.html', {'form': form, 'total_balance': account.total_balance_display, 'currency': currency})



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
            for deposite in deposits:
                deposite.added_funds = round(request.user.convert_price(deposite.added_funds, request.user.currency), 2)
                deposite.total_balance = round(request.user.convert_price(deposite.total_balance, request.user.currency), 2)

    return render(request, 'account/show_deposit.html', {'deposits': deposits, 'currency': request.user.currency})