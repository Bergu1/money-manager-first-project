from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models.functions import ExtractMonth, ExtractYear
from core.models import AccountHistory, Bills, DailyBuy, Random_expenses
from django.db.models import Sum
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from django.http import HttpResponse
import csv
from django.utils.encoding import smart_str
from django.db import transaction
from decimal import Decimal
from datetime import datetime

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
        'currency': person.currency,
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


@login_required
def generate_csv(request):
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
        month=month
    )
    total_expenses1 = expenses1.aggregate(total=Sum('price'))['total'] or 0
    total_expenses1 = person.convert_price(total_expenses1, person.currency)

    expenses2 = Bills.objects.annotate(
        month=ExtractMonth('date'),
        year=ExtractYear('date')
    ).filter(
        person=person,
        year=year,
        month=month
    )
    total_expenses2 = expenses2.aggregate(total=Sum('price'))['total'] or 0
    total_expenses2 = person.convert_price(total_expenses2, person.currency)

    expenses3 = Random_expenses.objects.annotate(
        month=ExtractMonth('date'),
        year=ExtractYear('date')
    ).filter(
        person=person,
        year=year,
        month=month
    )
    total_expenses3 = expenses3.aggregate(total=Sum('price'))['total'] or 0
    total_expenses3 = person.convert_price(total_expenses3, person.currency)

    total_expenses = round(total_expenses1 + total_expenses2 + total_expenses3, 2)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="savings_report_{month}_{year}.csv"'

    writer = csv.writer(response, delimiter=';')
    
    writer.writerow([
        smart_str("Date"), 
        smart_str("Description"),
        smart_str("Details"),
        smart_str("Shop"),
        smart_str("Amount"),
        smart_str("Currency"),
    ])

    for deposit in deposits:
        writer.writerow([
            smart_str(deposit.date), 
            smart_str("Deposit"),
            smart_str(deposit.source),
            smart_str(" "),
            smart_str(round(person.convert_price(deposit.added_funds, person.currency), 2)),
            smart_str(person.currency),
        ])

    for expense in expenses1:
        writer.writerow([
            smart_str(expense.date), 
            smart_str("Daily Buy"),
            smart_str(expense.product),
            smart_str(expense.shop),
            smart_str(round(person.convert_price(expense.price, person.currency), 2)),
            smart_str(person.currency),
        ])

    for expense in expenses2:
        writer.writerow([
            smart_str(expense.date), 
            smart_str("Bill"),
            smart_str(expense.fee),
            smart_str(" "),
            smart_str(round(person.convert_price(expense.price, person.currency), 2)),
            smart_str(person.currency),
        ])

    for expense in expenses3:
        writer.writerow([
            smart_str(expense.date), 
            smart_str("Random Expense"),
            smart_str(expense.for_what),
            smart_str(" "),
            smart_str(round(person.convert_price(expense.price, person.currency), 2)),
            smart_str(person.currency),
        ])

    writer.writerow([])
    writer.writerow([smart_str("Total Deposits"), smart_str(total_deposits)])
    writer.writerow([smart_str("Total Expenses"), smart_str(total_expenses)])

    return response


@login_required
def import_expenses_from_csv(request):
    if request.method == 'GET':
        return render(request, 'manager/upload_expenses_from_csv_file.html')

    if request.method != 'POST':
        return HttpResponse("Invalid request method. Please use POST.", status=400)

    csv_file = request.FILES.get('csv_file')
    if not csv_file:
        return HttpResponse("Please upload a CSV file.", status=400)

    person = request.user
    account = person.account  # Konto użytkownika
    user_currency = person.currency  # Waluta użytkownika

    try:
        decoded_file = csv_file.read().decode('utf-8-sig').splitlines()
        reader = csv.DictReader(decoded_file, delimiter=';')

        reader.fieldnames = [field.strip() for field in reader.fieldnames]
        print(f"Field names from CSV after stripping: {reader.fieldnames}")

        with transaction.atomic():
            for row_data in reader:
                try:
                    row = {key.strip(): value.strip() for key, value in row_data.items()}

                    # Pobieranie i walidacja daty
                    raw_date = row.get('Date', '')
                    if not raw_date:
                        return HttpResponse("Date field is missing or empty in the CSV.", status=400)

                    try:
                        date = datetime.strptime(raw_date, "%Y-%m-%d").date() 
                    except ValueError:
                        return HttpResponse(f"Invalid date format: {raw_date}. Expected format is YYYY-MM-DD.", status=400)

                    # Pobieranie reszty pól
                    description = row.get('Description', '')
                    details = row.get('Details', '')
                    shop = row.get('Shop', '')

                    if not row.get('Amount'):
                        return HttpResponse("Amount field is empty in the CSV.", status=400)

                    currency = row.get('Currency', '')

                    amount = Decimal(row.get('Amount'))

                    if currency != 'USD':
                        amount_in_usd = person.convert_price_write(amount, currency)  
                    else:
                        amount_in_usd = amount 

                    if description == "Daily Buy":
                        daily_buy = DailyBuy.objects.create(
                            person=person,
                            date=date,
                            product=details,
                            shop=shop,
                            price=amount_in_usd,  # Zapisujemy przeliczoną kwotę w USD
                        )
                    elif description == "Bill":
                        bill = Bills.objects.create(
                            person=person,
                            date=date,
                            fee=details,
                            price=amount_in_usd,  # Zapisujemy w USD
                        )
                    elif description == "Random Expense":
                        random_expense = Random_expenses.objects.create(
                            person=person,
                            date=date,
                            for_what=details,
                            price=amount_in_usd,  # Zapisujemy w USD
                        )

                    account.update_balance(amount_in_usd, operation="subtract")

                except KeyError as e:
                    return HttpResponse(f"Missing column in CSV: {e}", status=400)
                except ValueError:
                    return HttpResponse("Invalid data format in CSV.", status=400)
            
        return HttpResponse("Expenses imported successfully.", status=200)

    except Exception as e:
        return HttpResponse(f"Error processing the CSV file: {e}", status=500)
