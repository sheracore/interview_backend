from django.utils.deprecation import MiddlewareMixin


class UserInformationMiddleware(MiddlewareMixin):
    """
    Middleware that sets `User info` attribute to request object.
    """
    def process_request(self, request):
        user = request.user
        if user.is_authenticated:
            request.user_info = user.info()
        else:
            request.user_info = None
