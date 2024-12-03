# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Roadside_backend.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": 
#         URLRouter(
#             websocket_urlpatterns
#     ),
# })


import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import importlib

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Roadside_backend.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        importlib.import_module('chat_support.routing').websocket_urlpatterns
    ),
})
