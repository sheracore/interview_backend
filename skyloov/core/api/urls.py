from django.urls import path
from rest_framework import routers

from skyloov.core.files.api.views import FileViewSet
from skyloov.utilities.contenttypes.api.views import content_type_view

router = routers.DefaultRouter()
router.register('files', FileViewSet)
core_api_urlpatterns = router.urls

core_api_urlpatterns = core_api_urlpatterns + [
    path(r'content-type/', content_type_view),
]
