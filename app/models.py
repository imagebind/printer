from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import timedelta
from django.core.validators import RegexValidator

# Create your models here.

PLAN_CHOICES = {
    'Plan A': 'Plan A',
    'Plan B': 'Plan B',
    'Plan C': 'Plan C',
}

class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='districts')

    def __str__(self):
        return self.name    


class Plan(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    amount = models.IntegerField(null=False)
    duration = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100, null=True)
    cell_number = models.CharField(
        max_length=10, 
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")]
    )
    email = models.EmailField(unique=True)
    flat_no = models.CharField(max_length=10, null=True)
    flat_name = models.CharField(max_length=100, null=True)
    door_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    taluk = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE) 
    district =  models.ForeignKey(District, on_delete=models.CASCADE) 
    pincode = models.CharField(max_length=6)
    landmark = models.CharField(max_length=100, null=True)
    subscription_date = models.DateField(null=True)
    plan = models.ForeignKey(Plan, on_delete=models.DO_NOTHING)
    plan_expiration_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refer_by = models.CharField(max_length=100, null=True)
    bjp_membership_number = models.CharField(
        max_length=10, 
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")]
    )


    def __str__(self) -> str:
        return self.name


class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    payment_id = models.CharField(max_length=100, unique=True)
    order_id = models.CharField(max_length=100)
    signature = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.payment_id
    
@receiver(pre_save, sender=Customer)
def add_sku(sender, instance, **kwargs):
    instance.name = instance.name.upper()
    instance.father_name = instance.father_name.upper()
    instance.email = instance.email.upper()
    instance.taluk = instance.taluk.upper()
    if instance.subscription_date:
        instance.plan_expiration_date = instance.subscription_date + timedelta(weeks=52*instance.plan.duration)


