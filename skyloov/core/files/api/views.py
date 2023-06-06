from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from skyloov.utilities.api.paginations import StandardResultsSetPagination
from skyloov.utilities.api.views import UserDataModelViewSet
from skyloov.utilities.permissions import AllowStaff, IsSuperUserAccessPermission

# ViewSets define the view behavior.
from ..models import FileModel
from .filters import FileFilterSet
from .serializers import FileModelDetailSerializer, FileModelSummarySerializer

"""
File
"""


class FileViewSet(UserDataModelViewSet):
    model = FileModel
    queryset = FileModel.objects.none()
    pagination_class = StandardResultsSetPagination
    filterset_class = FileFilterSet
    OrderingFilter = ('type', 'size', 'title', 'status', 'created_at', 'update_at')

    serializers = {
        'default': FileModelSummarySerializer,
        'create': FileModelDetailSerializer,
        'update': FileModelDetailSerializer,
    }
    permission_classes_by_action = {
        'default': [
            IsSuperUserAccessPermission,
        ],
        'retrieve': [
            AllowAny,
        ],
        'list': [
            AllowAny,
        ],
        'create': [
            IsAuthenticated,
        ],
        'update': [
            AllowStaff,
        ],
    }

