# Generated by Django 5.1.2 on 2024-10-27 06:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_state_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.district'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.state'),
        ),
    ]
