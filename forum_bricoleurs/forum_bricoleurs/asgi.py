import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forum_bricoleurs.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Ajoute d'autres protocoles comme WebSockets ici si nécessaire
})
