# Generated by Django 5.1.6 on 2025-03-08 11:38

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0007_compartment1_taken_compartment1_taken_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompartmentHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taken', models.BooleanField(default=False)),
                ('taken_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('compartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='myapi.compartment1')),
            ],
        ),
    ]
