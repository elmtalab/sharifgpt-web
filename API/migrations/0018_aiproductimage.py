# Generated by Django 3.2.4 on 2024-01-18 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0017_aiproduct_aiproductfeature_aiproductreview'),
    ]

    operations = [
        migrations.CreateModel(
            name='AIProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/')),
                ('alt_text', models.CharField(blank=True, max_length=255)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='API.aiproduct')),
            ],
        ),
    ]
