from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from skyloov.users.models import UserInformation
from skyloov.utilities.permissions import AllowStaff, IsSuperUserAccessPermission
from skyloov.utilities.api.views import UserDataModelViewSet
from skyloov.utilities.api.paginations import StandardResultsSetPagination


# ViewSets define the view behavior.
from ..serializers import (
    UserInformationAdminSummarySerializer,
    UserInformationDetailSerializer,
    UserInformationSummarySerializer,
)


class UserInformationViewSet(UserDataModelViewSet):
    queryset = UserInformation.objects.none()
    pagination_class = StandardResultsSetPagination
    OrderingFilter = (
        'first_name',
        'last_name',
        'last_login',
        'is_staff',
        'email',
        'gender',
        'timezone',
        'language',
        'created_at',
        'update_at',
    )
    model = UserInformation

    serializers = {
        'default': UserInformationSummarySerializer,
        'retrieve': UserInformationDetailSerializer,
        'create': UserInformationDetailSerializer,
        'update': UserInformationDetailSerializer,
        'me': UserInformationDetailSerializer,
        'change_staff': UserInformationDetailSerializer,
        'admin': UserInformationAdminSummarySerializer,
        'filter_admin': UserInformationAdminSummarySerializer,
    }
    permission_classes_by_action = {
        'default': [
            IsSuperUserAccessPermission,
        ],
        'list': [
            AllowAny,
        ],
        'retrieve': [
            AllowAny,
        ],
        'update': [
            AllowStaff,
        ],
        'create': [
            AllowStaff,
        ],
        'destroy': [
            IsSuperUserAccessPermission,
        ],
        'me': [
            IsAuthenticated,
        ],
        'change_staff': [
            AllowStaff,
        ],
    }

    def perform_create(self, serializer, *args, **kwargs):
        user = self.get_user_perform_create()
        user_info_exists = self.model.objects.filter(user_id=user.pk).exists()
        if user_info_exists:
            raise ValidationError({
                "User": ["User information with this user exists"]
            })
        kwargs['user_id'] = user.pk
        super(UserDataModelViewSet, self).perform_create(serializer=serializer, **kwargs)

    @action(methods=['get', 'put'], detail=False)
    def me(self, request):
        user_info = self.get_queryset().get(user=request.user)
        if request.method in SAFE_METHODS:
            serializer = self.get_serializer(user_info, many=False, read_only=True, context={'request': request}).data
            return Response(serializer, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(user_info, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['put'],
        detail=True,
    )
    def change_staff(self, request, pk):
        if 'is_staff' not in request.data:
            raise ValidationError({
                'is_staff': ["is required"]
                }
            )
        obj = self.get_object()
        obj.is_staff = request.data.get('is_staff', False)
        obj.save()
        serializer = self.get_serializer(obj, many=False, read_only=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
