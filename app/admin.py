from django.contrib import admin

# Register your models here.

from .models import Plan, Customer, State, District, Payment

class StateAdmin(admin.ModelAdmin):
    # list_display = ['name', 'amount', 'duration']
    pass

class DistrictAdmin(admin.ModelAdmin):
    # list_display = ['name', 'amount', 'duration']
    pass

class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'duration']

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['customer', 'payment_id', 'order_id', 'amount', 'status', 'payment_method']
    pass

class CustomerAdmin(admin.ModelAdmin):
    list_display =  ['id', 'name', 'email', 'state', 'plan']
    list_filter  = ['state','plan']
    readonly_fields = ['plan_expiration_date']
    search_fields = ['name']


admin.site.register(Plan, PlanAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Payment, PaymentAdmin)


