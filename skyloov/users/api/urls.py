from rest_framework import routers
from ..api.views import UserInformationViewSet

router = routers.DefaultRouter()
router.register(r'users_info', UserInformationViewSet)

user_api_urlpatterns = router.urls
user_api_urlpatterns = user_api_urlpatterns + []
