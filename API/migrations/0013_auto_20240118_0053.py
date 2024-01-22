# Generated by Django 3.2.4 on 2024-01-17 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0012_eventpaymentrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentrecord',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='API.event'),
        ),
        migrations.AlterField(
            model_name='paymentrecord',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='API.course'),
        ),
    ]
