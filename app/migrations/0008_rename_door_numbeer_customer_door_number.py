# Generated by Django 5.1.2 on 2024-10-27 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_customer_district_alter_customer_state'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='door_number',
            new_name='door_number',
        ),
    ]
