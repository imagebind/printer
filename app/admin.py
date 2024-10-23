from django.contrib import admin

# Register your models here.

from .models import Plan, Customer

class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'duration']


class CustomerAdmin(admin.ModelAdmin):
    list_display =  ['id', 'name', 'email', 'state', 'plan']
    list_filter  = ['state','plan', 'district']
    readonly_fields = ['plan_expiration_date']
    search_fields = ['name']


admin.site.register(Plan, PlanAdmin)
admin.site.register(Customer, CustomerAdmin)