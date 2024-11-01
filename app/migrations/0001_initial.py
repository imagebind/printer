# Generated by Django 5.1.2 on 2024-10-21 15:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('amount', models.IntegerField()),
                ('duration', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('father_name', models.CharField(max_length=100)),
                ('cell_number', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('flat_no', models.CharField(max_length=10)),
                ('flat_name', models.CharField(max_length=100)),
                ('door_number', models.CharField(max_length=10)),
                ('street_name', models.CharField(max_length=100)),
                ('area', models.CharField(max_length=100)),
                ('taluk', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('pincode', models.IntegerField(max_length=6)),
                ('landmark', models.CharField(max_length=100)),
                ('subscription_date', models.DateField()),
                ('plan_expiration_date', models.DateField()),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.plan')),
            ],
        ),
    ]
