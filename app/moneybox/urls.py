from django.urls import path
from .views import set_savings_goal, transfer_to_savings, cash_out

urlpatterns = [
    path('set_savings_goal/', set_savings_goal, name='set_savings_goal'),
    path('transfer_to_savings/', transfer_to_savings, name='transfer_to_savings'),
    path('cash_out/', cash_out, name='cash_out'),
]
