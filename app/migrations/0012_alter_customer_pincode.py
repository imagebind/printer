# Generated by Django 5.1.2 on 2024-10-29 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='pincode',
            field=models.IntegerField(),
        ),
    ]
