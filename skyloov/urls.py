from .users.urls import users_urlpatterns
from .core.urls import core_urlpatterns

skyloov_urlpatterns = (
    users_urlpatterns + core_urlpatterns
)
