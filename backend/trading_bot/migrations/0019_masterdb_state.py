# Generated by Django 4.1.4 on 2023-04-25 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading_bot', '0018_masterdb_balanceasset_masterdb_balancecash_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='masterdb',
            name='state',
            field=models.CharField(default='', max_length=30),
        ),
    ]