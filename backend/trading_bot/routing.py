from . import consumers
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'ws/trading-bot/$', consumers.TradingBotConsumer().as_asgi())
]
