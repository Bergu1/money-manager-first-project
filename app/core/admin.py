from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['id', 'first_name', 'last_name', 
                    'username', 'email', 'date_of_birth', 'account']
    fieldsets = (
        (None, {"fields": ('username', 'email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'first_name',
                'last_name',
                'username',
                'email',
                'date_of_birth',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )


class DailyBuyAdmin(admin.ModelAdmin):
    list_display = ('day', 'date', 'shop', 'product', 'price', 'person')
    search_fields = ('shop', 'product', 'person__username')
    list_filter = ('day', 'date', 'shop')


class BillsAdmin(admin.ModelAdmin):
    list_display = ('date', 'fee', 'price', 'person')
    search_fields = ('fee', 'person__username')
    list_filter = ('date',)


class RandomExpensesAdmin(admin.ModelAdmin):
    list_display = ('date', 'for_what', 'price', 'person')
    search_fields = ('for_what', 'person__username')
    list_filter = ('date',)


class AccountAdmin(admin.ModelAdmin):
    list_display = ('id','date', 'added_funds', 'total_balance', 'source')
    search_fields = ('source',)
    list_filter = ('date',)

class AccountHistoryAdmin(admin.ModelAdmin):
    list_display = ('account', 'date', 'added_funds', 'total_balance', 'source', 'timestamp')
    search_fields = ('account__id', 'source')
    list_filter = ('date', 'timestamp')


admin.site.register(models.Person, UserAdmin)
admin.site.register(models.DailyBuy, DailyBuyAdmin)
admin.site.register(models.Bills, BillsAdmin)
admin.site.register(models.Random_expenses, RandomExpensesAdmin)
admin.site.register(models.Account, AccountAdmin)
admin.site.register(models.AccountHistory, AccountHistoryAdmin)