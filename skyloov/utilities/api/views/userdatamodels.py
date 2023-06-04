from skyloov.utilities.api.filters import UserDataModelFilterSet
from ..serializers import UserDataModelDetailSerializer
from .datamodels import DataModelViewSet

"""
User Data Model
"""


class UserDataModelViewSet(DataModelViewSet):
    serializers = {
        'default': UserDataModelDetailSerializer,
    }
    filterset_class = UserDataModelFilterSet

    def perform_create(self, serializer, *args, **kwargs):
        user = self.get_user_perform_create()
        kwargs['user_id'] = user.pk
        super(UserDataModelViewSet, self).perform_create(serializer=serializer, **kwargs)

    def get_user_perform_create(self):
        user = self.request.user
        return user

    def get_queryset(self):
        return super(UserDataModelViewSet, self).get_queryset()
