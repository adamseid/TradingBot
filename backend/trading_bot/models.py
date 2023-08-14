from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=255, blank=True, null=True)
    api_secret = models.CharField(max_length=255, blank=True, null=True)

    
class ClientData(models.Model):
    roomGroupName = models.CharField(max_length=30, unique=True)
    timeframe = models.CharField(max_length=30, default='1h')
    location = models.CharField(max_length=30, default='')
    selection = models.CharField(max_length=30, default='')


class MasterDB(models.Model):
    selectionMenu = models.CharField(max_length=30, default='')

    raw = models.CharField(max_length=30, default='')
    analysis = models.CharField(max_length=30, default='')
    simulation = models.CharField(max_length=30, default='')

    unix = models.CharField(max_length=30, default='')

    time = models.CharField(max_length=30, default='')
    price = models.CharField(max_length=30, default='')
    dprice = models.CharField(max_length=30, default='')
    volume = models.CharField(max_length=30, default='')
    momentum = models.CharField(max_length=30, default='')
    momentumStdev = models.CharField(max_length=30, default='')

    dpriceStdev = models.CharField(max_length=30, default='')

    state = models.CharField(max_length=30, default='')
    balanceCash = models.CharField(max_length=30, default='')
    balanceAsset = models.CharField(max_length=30, default='')
    value = models.CharField(max_length=30, default='')

    deltaT = models.CharField(max_length=30, default='')
    rValue = models.CharField(max_length=30, default='')

    balanceShort = models.CharField(max_length=30, default='')
    balanceLong = models.CharField(max_length=30, default='')

    prev_trade_unix = models.CharField(max_length=30, default='')
    profit = models.CharField(max_length=30, default='')
    profit_percent = models.CharField(max_length=30, default='')


class Raw(models.Model):
    time = models.CharField(max_length=30, default='')
    unix = models.CharField(max_length=30, default='')
    price = models.CharField(max_length=30, default='')
    volume = models.CharField(max_length=30, default='')


class BTCUSDT_PERP(models.Model):
    time = models.CharField(max_length=30, default='')
    unix = models.CharField(max_length=30, default='')
    price = models.CharField(max_length=30, default='')
    volume = models.CharField(max_length=30, default='')
