from django.shortcuts import render, redirect
from django.template import loader
from .forms import DailyBuyForm, RandomExpensesForm, BillsForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models.functions import ExtractMonth, ExtractYear
from django.template.loader import get_template
from core.models import Account


@login_required
def daily_buy(request):
    account = request.user.account
    if request.method == 'POST':
        form = DailyBuyForm(request.POST)
        if form.is_valid():
            daily_buy = form.save(commit=False)
            daily_buy.person = request.user
            daily_buy.save()
            account.update_balance(daily_buy.price, "subtract")
            return redirect('daily_buy')
    else:
        form = DailyBuyForm()

    return render(request, 'expenses/daily_buy.html', {'form': form})


@login_required
def bills(request):
    account = request.user.account
    if request.method == 'POST':
        form = BillsForm(request.POST)
        if form.is_valid():
            bills = form.save(commit=False)
            bills.person = request.user
            bills.save()
            account.update_balance(bills.price, "subtract")
            return redirect('bills')
    else:
        form = BillsForm()

    return render(request, 'expenses/bills.html', {'form': form})


@login_required
def random_expenses(request):
    account = request.user.account
    if request.method == 'POST':
        form = RandomExpensesForm(request.POST)
        if form.is_valid():
            random_expenses = form.save(commit=False)
            random_expenses.person = request.user 
            random_expenses.save()
            account.update_balance(random_expenses.price, "subtract")
            return redirect('random_expenses')
    else:
        form = RandomExpensesForm()

    return render(request, 'expenses/random_expenses.html', {'form': form})