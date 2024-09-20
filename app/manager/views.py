from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models.functions import ExtractMonth, ExtractYear
from core.models import AccountHistory, Bills, DailyBuy, Random_expenses
from django.db.models import Sum
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from django.http import HttpResponse

@login_required
def savings_manager(request):
    user = request.user
    user1 = request.user.account
    deposit = None
    expenses = None
    expenses1 = None
    expenses2 = None
    expenses3 = None
    total_expenses0 = 0
    if request.method == 'POST':
        month = int(request.POST.get('month'))
        year = int(request.POST.get('year'))
        if month and year:
            deposit = AccountHistory.objects.annotate(
                month=ExtractMonth('date'),
                year=ExtractYear('date')
            ).filter(
                account=user1,
                year=year,
                month=month,
                added_funds__gt=0  
            )

            total_expenses0 = deposit.aggregate(total=Sum('added_funds'))['total'] or 0
            total_expenses0 = user.convert_price(total_expenses0, user.currency)
            total_expenses0 = round(total_expenses0, 2)

            expenses1 = DailyBuy.objects.annotate(
                month=ExtractMonth('date'),
                year=ExtractYear('date')
            ).filter(
                person=user,
                year=year,
                month=month, 
            )

            total_expenses1 = expenses1.aggregate(total=Sum('price'))['total'] or 0
            total_expenses1 = user.convert_price(total_expenses1, user.currency)

            expenses2 = Bills.objects.annotate(
                month=ExtractMonth('date'),
                year=ExtractYear('date')
            ).filter(
                person=user,
                year=year,
                month=month, 
            )

            total_expenses2 = expenses2.aggregate(total=Sum('price'))['total'] or 0
            total_expenses2 = user.convert_price(total_expenses2, user.currency)

            expenses3 = Random_expenses.objects.annotate(
                month=ExtractMonth('date'),
                year=ExtractYear('date')
            ).filter(
                person=user,
                year=year,
                month=month, 
            )

            for transaction in deposit:
                transaction.added_funds = round(user.convert_price(transaction.added_funds, user.currency), 2)
                transaction.total_balance = round(user.convert_price(transaction.total_balance, user.currency), 2)

            for expense in expenses1:
                expense.price = round(user.convert_price(expense.price, user.currency), 2)
            
            for expense in expenses2:
                expense.price = round(user.convert_price(expense.price, user.currency), 2)
            
            for expense in expenses3:
                expense.price = round(user.convert_price(expense.price, user.currency), 2)

            total_expenses3 = expenses3.aggregate(total=Sum('price'))['total'] or 0
            total_expenses3 = user.convert_price(total_expenses3, user.currency)

            expenses = total_expenses1 + total_expenses2 + total_expenses3
            expenses = round(expenses, 2)

    return render(request, 'manager/savings_manager.html', {'deposits' : deposit, 'expenses1' : expenses1, 'expenses2' : expenses2,
                                                     'expenses3' : expenses3, 'expenses' : expenses, 'total_expenses0' : total_expenses0,
                                                       'currency': user.currency})


@login_required
def purchase_list(request):
    user = request.user
    purchases = None
    purchases2 = None
    purchases3 = None
    if request.method == 'POST':
        date = request.POST.get('date')
        if date:
            purchases = DailyBuy.objects.filter(date=date, person=user)
            purchases2 = Bills.objects.filter(date=date, person=user)
            purchases3 = Random_expenses.objects.filter(date=date, person=user)

            for expense in purchases:
                expense.price = round(user.convert_price(expense.price, user.currency), 2)
            
            for expense in purchases2:
                expense.price = round(user.convert_price(expense.price, user.currency), 2)
            
            for expense in purchases3:
                expense.price = round(user.convert_price(expense.price, user.currency), 2)

    return render(request, 'manager/expenses_manager.html', {'purchases': purchases, 'purchases2': purchases2,
                                                              'purchases3': purchases3, 'currency': user.currency})



@login_required
def generate_pdf(request):
    if request.method != 'POST':
        return HttpResponse("Invalid request method. Please use POST.", status=400)
    
    person = request.user 

    try:
        month = int(request.POST.get('month'))
        year = int(request.POST.get('year'))
    except (TypeError, ValueError):
        return HttpResponse("Invalid month or year. Please provide valid integers.", status=400)

    if not (month and year):
        return HttpResponse("Month and year are required.", status=400)

    deposits = AccountHistory.objects.annotate(
        month=ExtractMonth('date'),
        year=ExtractYear('date')
    ).filter(
        account=person.account,
        year=year,
        month=month,
        added_funds__gt=0  
    )
    total_deposits = deposits.aggregate(total=Sum('added_funds'))['total'] or 0
    total_deposits = round(person.convert_price(total_deposits, person.currency), 2)

    expenses1 = DailyBuy.objects.annotate(
        month=ExtractMonth('date'),
        year=ExtractYear('date')
    ).filter(
        person=person,
        year=year,
        month=month, 
    )
    total_expenses1 = expenses1.aggregate(total=Sum('price'))['total'] or 0
    total_expenses1 = person.convert_price(total_expenses1, person.currency)

    expenses2 = Bills.objects.annotate(
        month=ExtractMonth('date'),
        year=ExtractYear('date')
    ).filter(
        person=person,
        year=year,
        month=month, 
    )
    total_expenses2 = expenses2.aggregate(total=Sum('price'))['total'] or 0
    total_expenses2 = person.convert_price(total_expenses2, person.currency)

    expenses3 = Random_expenses.objects.annotate(
        month=ExtractMonth('date'),
        year=ExtractYear('date')
    ).filter(
        person=person,
        year=year,
        month=month, 
    )
    total_expenses3 = expenses3.aggregate(total=Sum('price'))['total'] or 0
    total_expenses3 = person.convert_price(total_expenses3, person.currency)
    total_expenses = round(total_expenses1 + total_expenses2 + total_expenses3, 2)

    context = {
        'person': person,
        'month': month,
        'year': year,
        'total_deposits': total_deposits,
        'total_expenses1': total_expenses1,
        'total_expenses2': total_expenses2,
        'total_expenses3': total_expenses3,
        'total_expenses': total_expenses,
        'deposits': deposits,
        'expenses1': expenses1,
        'expenses2': expenses2,
        'expenses3': expenses3,
    }

    html = render_to_string('manager/pdf_template.html', context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="savings_report_{month}_{year}.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('An error occurred while generating the PDF', status=500)
    return response


@login_required
def set_currency(request):
    if request.method == 'POST':
        currency = request.POST.get('currency')
        request.user.currency = currency
        request.user.save()
        return redirect('mainPage')
    else:
        return redirect('mainPage')
