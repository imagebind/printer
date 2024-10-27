from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import timedelta


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
    father_name = models.CharField(max_length=100)
    cell_number = models.IntegerField()
    email = models.EmailField(unique=True)
    flat_no = models.CharField(max_length=10)
    flat_name = models.CharField(max_length=100)
    door_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    taluk = models.CharField(max_length=100)
    district =  models.ForeignKey(District, on_delete=models.CASCADE) 
    state = models.ForeignKey(State, on_delete=models.CASCADE) 
    pincode = models.IntegerField(max_length=6)
    landmark = models.CharField(max_length=100)
    subscription_date = models.DateField()
    plan = models.ForeignKey(Plan, on_delete=models.DO_NOTHING)
    plan_expiration_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.name



@receiver(pre_save, sender=Customer)
def add_sku(sender, instance, **kwargs):
    instance.name = instance.name.upper()
    instance.father_name = instance.father_name.upper()
    instance.email = instance.email.upper()
    instance.state = instance.state.upper()
    instance.district = instance.district.upper()
    instance.taluk = instance.taluk.upper()
    instance.plan_expiration_date = instance.subscription_date + timedelta(weeks=52*instance.plan.duration)


