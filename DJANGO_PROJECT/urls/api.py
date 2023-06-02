from rest_framework import routers

from skyloov.api.urls import skyloov_api_urlpatterns

router = routers.DefaultRouter()

api_url = router.urls
api_url = api_url + skyloov_api_urlpatterns
