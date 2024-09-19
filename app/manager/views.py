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

            expenses1 = DailyBuy.objects.annotate(
                month=ExtractMonth('date'),
                year=ExtractYear('date')
            ).filter(
                person=user,
                year=year,
                month=month, 
            )

            total_expenses1 = expenses1.aggregate(total=Sum('price'))['total'] or 0

            expenses2 = Bills.objects.annotate(
                month=ExtractMonth('date'),
                year=ExtractYear('date')
            ).filter(
                person=user,
                year=year,
                month=month, 
            )

            total_expenses2 = expenses2.aggregate(total=Sum('price'))['total'] or 0

            expenses3 = Random_expenses.objects.annotate(
                month=ExtractMonth('date'),
                year=ExtractYear('date')
            ).filter(
                person=user,
                year=year,
                month=month, 
            )

            total_expenses3 = expenses3.aggregate(total=Sum('price'))['total'] or 0

            expenses = total_expenses1 + total_expenses2 + total_expenses3

    return render(request, 'manager/savings_manager.html', {'deposits' : deposit, 
                                                            'expenses1' : expenses1, 
                                                            'expenses2' : expenses2, 
                                                            'expenses3' : expenses3, 
                                                            'expenses' : expenses, 
                                                            'total_expenses0' : total_expenses0})


@login_required
def purchase_list(request):
    purchases = None
    purchases2 = None
    purchases3 = None
    if request.method == 'POST':
        date = request.POST.get('date')
        if date:
            purchases = DailyBuy.objects.filter(date=date, person=request.user)
            purchases2 = Bills.objects.filter(date=date, person=request.user)
            purchases3 = Random_expenses.objects.filter(date=date, person=request.user)

    return render(request, 'manager/expenses_manager.html', {'purchases': purchases, 'purchases2': purchases2, 'purchases3': purchases3})



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

    # Pobranie wszystkich wydatków
    expenses1 = DailyBuy.objects.annotate(
        month=ExtractMonth('date'),
        year=ExtractYear('date')
    ).filter(
        person=person,
        year=year,
        month=month, 
    )
    total_expenses1 = expenses1.aggregate(total=Sum('price'))['total'] or 0

    expenses2 = Bills.objects.annotate(
        month=ExtractMonth('date'),
        year=ExtractYear('date')
    ).filter(
        person=person,
        year=year,
        month=month, 
    )
    total_expenses2 = expenses2.aggregate(total=Sum('price'))['total'] or 0

    expenses3 = Random_expenses.objects.annotate(
        month=ExtractMonth('date'),
        year=ExtractYear('date')
    ).filter(
        person=person,
        year=year,
        month=month, 
    )
    total_expenses3 = expenses3.aggregate(total=Sum('price'))['total'] or 0

    total_expenses = total_expenses1 + total_expenses2 + total_expenses3

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
