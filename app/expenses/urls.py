from django.contrib.auth.decorators import login_required
from django.urls import path, include
from . import views


urlpatterns = [
    path('daily_buy/', views.daily_buy, name='daily_buy'),
    path('bills/', views.bills, name='bills'),
    path('random_expenses/', views.random_expenses, name='random_expenses'),
]