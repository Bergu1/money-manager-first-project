from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from django.utils import timezone
from decimal import Decimal
import requests


class PersonManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        account = Account.objects.create(
            date=timezone.now(),
            total_balance=0
        )

        person = self.model(username=username,
                            email=self.normalize_email(email),
                            account=account,
                            **extra_fields)
        person.set_password(password)
        person.save(using=self._db)

        return person

    def create_superuser(self, username, email, password=None, **extra_fields):
        person = self.create_user(username, email, password, **extra_fields)
        person.is_staff = True
        person.is_superuser = True
        person.save(using=self._db)  # Poprawione: "self.db" zmienione na "self._db"
        return person


class Person(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=80, unique=True)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    account = models.OneToOneField('Account', on_delete=models.CASCADE, null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD')


    objects = PersonManager()

    class Meta:
        verbose_name = 'Person' 
        verbose_name_plural = 'Persons'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


    def get_exchange_rate(self, base_currency, target_currency):
        api_key = 'f193fd51d73d8997215547c8'
        url = f"https://v6.exchangerate-api.com/v6/f193fd51d73d8997215547c8/latest/USD"
        response = requests.get(url)
        data = response.json()
        return Decimal(data['conversion_rates'].get(target_currency, 1))


    def get_exchange_rate_write(self, base_currency, target_currency):
        api_key = 'f193fd51d73d8997215547c8'
        url = f"https://v6.exchangerate-api.com/v6/f193fd51d73d8997215547c8/latest/USD"
        response = requests.get(url)
        data = response.json()
        rate = Decimal(data['conversion_rates'].get(target_currency, 1))
        if target_currency == 'USD':
            return rate
        else:
            return 1 / rate


    def convert_price(self, price, user_currency):
        base_currency = 'USD'
        if user_currency != base_currency:
            rate = self.get_exchange_rate(base_currency, user_currency)
            rate = Decimal(rate)
            return price * rate
        return price


    def convert_price_write(self, price, user_currency):
        base_currency = 'USD'
        if user_currency != base_currency:
            rate = self.get_exchange_rate_write(base_currency, user_currency)
            rate = Decimal(rate)
            return price * rate
        return price


    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class DailyBuy(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    date = models.DateField()
    shop = models.CharField(max_length=100)
    product = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Daily Buy'
        verbose_name_plural = 'Daily Buy'

    def __str__(self):
        return f'{self.day} - {self.product} ({self.price})'


class Bills(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    fee = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Bill'
        verbose_name_plural = 'Bills'

    def __str__(self):
        return f'{self.date} - {self.fee} ({self.price})'


class Random_expenses(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    for_what = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Random Expenses'
        verbose_name_plural = 'Random Expenses'

    def __str__(self):
        return f'{self.date} - {self.for_what} ({self.price})'


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    added_funds = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    source = models.CharField(max_length=100, default='Unknown')

    def update_balance(self, amount, operation="add"):
        """ Aktualizacja bilansu konta. """
        print(f"Before updating balance: Current balance: {self.total_balance}, Amount: {amount}, Operation: {operation}")
        if operation == "add":
            self.total_balance += amount
            self.added_funds = amount
            self.save_to_history(operation="add")
        elif operation == "subtract":
            self.total_balance -= amount
            self.save_to_history(operation="subtract")
        print(f"After updating balance: New balance: {self.total_balance}")

    def save_to_history(self, *args, **kwargs):
        """ Zapisuje historię transakcji na koncie. """
        operation = kwargs.pop('operation', None)
        if operation == "add":
            AccountHistory.objects.create(
                account=self,
                date=self.date,
                added_funds=self.added_funds,
                total_balance=self.total_balance,
                source=self.source,
            )
        super(Account, self).save(*args, **kwargs)
        
    def __str__(self):
        return f'Account created on {self.date} - Balance: {self.total_balance}'


class AccountHistory(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, default=0)
    date = models.DateField()
    added_funds = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    source = models.CharField(max_length=100, default='Unknown')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'History for Account on {self.date} - Balance: {self.total_balance}'
    

class SavingsGoal(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Savings Goal"
