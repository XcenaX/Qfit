# from django.urls import path
# from channels.routing import ProtocolTypeRouter, URLRouter
# from . import consumers

# application = ProtocolTypeRouter({
#     "websocket": URLRouter([
#         path("ws/timers/", consumers.TimersConsumer.as_asgi()),
#     ]),
# })


# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path("ws/timers/", consumers.TimersConsumer.as_asgi()),
]

# from channels.routing import route
# from .consumers import websocket_receive

# channel_routing = [
#     route("websocket.receive", websocket_receive, path=r"^/sockets/chat/"),
# ]