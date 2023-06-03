from django.urls import path

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from .api.views import UserView

app_name='users'

users_urlpatterns = [
	path('api/token_auth/', obtain_jwt_token),
	path('api/token_refresh/', refresh_jwt_token),
	path('api/token_verify/', verify_jwt_token),
	path('api/users_register/', UserView.as_view(), name='users_register'),
]