# Generated by Django 4.1.4 on 2023-03-24 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading_bot', '0012_clientdata_selectionmenu'),
    ]

    operations = [
        migrations.AddField(
            model_name='masterdb',
            name='analysis',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='masterdb',
            name='selectionMenu',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='masterdb',
            name='simulation',
            field=models.CharField(default='', max_length=30),
        ),
    ]
