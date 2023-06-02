from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, AllowAny
from rest_framework.response import Response
from skyloov.users.models import User, UserInformation
from skyloov.utilities.permissions import AllowStaff, IsSuperUserAccessPermission
from skyloov.utilities.api.views import UserDataModelViewSet


# ViewSets define the view behavior.
from ..serializers import (
    UserInformationAdminSummarySerializer,
    UserInformationDetailSerializer,
    UserInformationSummarySerializer,
)


class UserInformationViewSet(UserDataModelViewSet):
    queryset = UserInformation.objects.none()
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

    @action(methods=['get', 'put'], detail=False, permission_classes=[IsAuthenticated])
    def me(self, request):
        user_info = request.user_info
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
        obj = self.get_object()
        if request.provider.user == obj.user:
            raise PermissionDenied
        obj.is_staff = request.data.get('is_staff', False)
        obj.save()
        serializer = self.get_serializer(obj, many=False, read_only=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
