from rest_framework import routers
from skyloov.shops.products.api.views import ProductViewSet
from skyloov.shops.carts.api.views import CartViewSet

routers = routers.DefaultRouter()

routers.register('products', ProductViewSet)
routers.register('carts', CartViewSet)

shops_api_urlpatterns = routers.urls
