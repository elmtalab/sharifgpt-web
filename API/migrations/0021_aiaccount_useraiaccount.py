# Generated by Django 3.2.4 on 2024-01-18 19:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0020_paymentrecord_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAIAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('instructions', models.TextField()),
                ('ai_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_accounts', to='API.aiproduct')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_ai_accounts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AIAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ai_accounts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
