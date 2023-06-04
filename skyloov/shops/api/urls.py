from rest_framework import routers
from skyloov.shops.products.api.views import ProductViewSet

routers = routers.DefaultRouter()

routers.register('products', ProductViewSet)

shops_api_urlpatterns = routers.urls
