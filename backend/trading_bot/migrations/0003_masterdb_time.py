# Generated by Django 4.1.4 on 2023-03-09 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading_bot', '0002_masterdb_unix'),
    ]

    operations = [
        migrations.AddField(
            model_name='masterdb',
            name='time',
            field=models.CharField(default='', max_length=30),
        ),
    ]
