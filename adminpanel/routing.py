# from django.urls import path
# from channels.routing import ProtocolTypeRouter, URLRouter
# from . import consumers

# application = ProtocolTypeRouter({
#     "websocket": URLRouter([
#         path("ws/timers/", consumers.TimersConsumer.as_asgi()),
#     ]),
# })

from . import consumers

channel_routing = {
    'websocket.connect': consumers.ws_connect,
    'websocket.receive': consumers.ws_receive,
    'websocket.disconnect': consumers.ws_disconnect,
}

# from channels.routing import route
# from .consumers import websocket_receive

# channel_routing = [
#     route("websocket.receive", websocket_receive, path=r"^/sockets/chat/"),
# ]