from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser

schema_view = get_schema_view(
    openapi.Info(
        title="SKYLOOV API",
        default_version='v1',
        description="",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="m.ghaffari662@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    permission_classes=[IsAdminUser],
    authentication_classes=[SessionAuthentication],
    public=True,
)

core_urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
