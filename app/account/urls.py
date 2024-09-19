from django.urls import path
from . import views


urlpatterns = [
    path('person_account/', views.account, name='account'),
    path('show_deposit/', views.show_deposit, name='show_deposit'),
]