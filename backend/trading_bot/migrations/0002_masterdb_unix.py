# Generated by Django 4.1.4 on 2023-03-09 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading_bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='masterdb',
            name='unix',
            field=models.CharField(default='', max_length=30),
        ),
    ]
