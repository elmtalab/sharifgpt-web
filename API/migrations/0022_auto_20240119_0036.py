# Generated by Django 3.2.4 on 2024-01-18 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0021_aiaccount_useraiaccount'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='duration_icon_url',
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='level_icon_url',
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
        migrations.DeleteModel(
            name='AIAccount',
        ),
    ]
