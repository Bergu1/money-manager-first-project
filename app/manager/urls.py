from django.contrib.auth.decorators import login_required
from django.urls import path, include
from . import views


urlpatterns = [
    path('savings_manager/', views.savings_manager, name='savings_manager'),
    path('purchases/', views.purchase_list, name='expenses_manager'),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
    path('set_currency/', views.set_currency, name='set_currency'),
    path('generate-csv/', views.generate_csv, name='generate_csv'),
    path('upload-from-file/', views.import_expenses_from_csv, name='upload-from-file'),
]