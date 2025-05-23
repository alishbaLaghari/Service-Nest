# Generated by Django 5.0.6 on 2024-07-13 21:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_customerdetails_accepted'),
        ('service_provider', '0003_remove_serviceproviderdetails_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.TextField()),
                ('customer_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customerdetails')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.request')),
                ('service_provider_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service_provider.serviceproviderdetails')),
            ],
        ),
    ]
