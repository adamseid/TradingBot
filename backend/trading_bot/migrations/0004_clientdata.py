# Generated by Django 4.1.4 on 2023-03-10 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading_bot', '0003_masterdb_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomGroupName', models.CharField(max_length=30, unique=True)),
                ('timeFrame', models.CharField(default='1h', max_length=30)),
            ],
        ),
    ]
