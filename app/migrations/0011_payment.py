# Generated by Django 5.1.2 on 2024-10-29 17:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_customer_plan_expiration_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(max_length=100)),
                ('order_id', models.CharField(max_length=100)),
                ('signature', models.CharField(max_length=100)),
                ('amount', models.CharField(max_length=100)),
                ('payment_method', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.customer')),
            ],
        ),
    ]
