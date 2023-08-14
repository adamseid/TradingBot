from django.contrib import admin
from .models import MasterDB, ClientData, Raw, BTCUSDT_PERP, UserProfile

# Register your models here.
admin.site.register(ClientData)
admin.site.register(MasterDB)
admin.site.register(Raw)
admin.site.register(BTCUSDT_PERP)
admin.site.register(UserProfile)
