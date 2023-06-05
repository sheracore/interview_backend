from skyloov.users.api.urls import user_api_urlpatterns
from skyloov.shops.api.urls import shops_api_urlpatterns
from skyloov.core.api.urls import core_api_urlpatterns

skyloov_api_urlpatterns = (
    user_api_urlpatterns
    + shops_api_urlpatterns
    + core_api_urlpatterns
)
