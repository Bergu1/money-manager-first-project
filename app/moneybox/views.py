from django.shortcuts import render, redirect
from .forms import SavingsGoalForm, TransferToSavingsForm
from core.models import SavingsGoal
from django.contrib.auth.decorators import login_required

@login_required
def set_savings_goal(request):
    try:
        savings_goal = SavingsGoal.objects.get(person=request.user)
    except SavingsGoal.DoesNotExist:
        savings_goal = None

    if request.method == 'POST':
        form = SavingsGoalForm(request.POST, instance=savings_goal)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.person = request.user
            goal.save()
            return redirect('transfer_to_savings')
    else:
        form = SavingsGoalForm(instance=savings_goal)

    user_currency = request.user.currency
    return render(request, 'moneybox/set_savings_goal.html', {
        'form': form,
        'currency': user_currency
    })

@login_required
def transfer_to_savings(request):
    account = request.user.account
    try:
        savings_goal = SavingsGoal.objects.get(person=request.user)
    except SavingsGoal.DoesNotExist:
        return redirect('set_savings_goal') 

    if request.method == 'POST':
        form = TransferToSavingsForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            amount_converted = request.user.convert_price_write(amount, request.user.currency)

            if amount_converted <= account.total_balance:
                account.update_balance(amount_converted, "subtract")
                savings_goal.current_amount += amount_converted
                savings_goal.save()
                return redirect('transfer_to_savings')
            else:
                form.add_error('amount', 'Lack of money on your account.')
    else:
        form = TransferToSavingsForm()

    user_currency = request.user.currency
    current_amount_converted = round(request.user.convert_price(savings_goal.current_amount, user_currency), 2)
    target_amount_converted = round(request.user.convert_price(savings_goal.target_amount, user_currency), 2)

    if savings_goal.target_amount > 0:
        savings_progress = round((savings_goal.current_amount / savings_goal.target_amount) * 100, 2)
    else:
        savings_progress = 0

    return render(request, 'moneybox/transfer_to_savings.html', {
        'form': form,
        'savings_goal': savings_goal,
        'current_amount': current_amount_converted,
        'target_amount': target_amount_converted,
        'currency': user_currency,
        'savings_progress': savings_progress
    })
