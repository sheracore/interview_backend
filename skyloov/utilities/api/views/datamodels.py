from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from skyloov.utilities.permissions import AllowOwner, AllowStaff

from ..serializers import DataModelDetailSerializer

"""
Data Model
"""


class DataModelViewSet(ModelViewSet):
    serializers = {
        'default': DataModelDetailSerializer,
    }
    permission_classes_by_action = {}

    def get_permissions(self):
        permissions = self.get_permission_classes_by_action()
        act = self.action
        permission_list = [permission() for permission in permissions.get(act, permissions['default'])]
        return permission_list

    def get_serializer_class(self):
        #TODO: bulk_create should be added
        self.serializers['bulk_create'] = self.serializers.get('create')
        return self.serializers.get(self.action, self.serializers['default'])

    @classmethod
    def get_permission_classes_by_action(cls):
        # TODO: handle stupid permission controlling
        permissions = {
            'default': [
                AllowStaff,
            ],
            'list': [
                AllowStaff,
            ],
            'retrieve': [
                AllowStaff,
            ],
            'create': [
                AllowOwner,
            ],
            'update': [
                AllowStaff,
            ],
            'partial_update': [
                AllowStaff,
            ],
            'destroy': [
                AllowStaff,
            ],
            'filter': [
                AllowAny,
            ],
            'filter_admin': [
                AllowStaff,
            ],
            'admin': [
                AllowStaff,
            ],
            'change_active': [
                AllowStaff,
            ],
            'bulk_delete': [
                AllowStaff,
            ],
            'bulk_update': [
                AllowOwner,
            ],
        }

        permissions['partial_update'] = permissions['update']
        permissions.update(cls.permission_classes_by_action)
        # حتما باید بعد از آپدیت باشد بخاطر اینکه پرمیشن برابر با کریت است وکریت
        # در هر کلاس مقدار دهی می شود اگر خط بالا باشد ما این مقدار را گم خواهیم کرد
        permissions['batch'] = permissions['create']
        return permissions

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(**kwargs)

    def is_admin(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        user_info = self.request.user_info
        return user_info.is_staff

    def get_queryset(self):
        if self.is_admin():
            return self.model.objects.all()
        return self.model.objects.active()

    def destroy(self, request, *args, **kwargs):
        item = self.get_object()
        try:
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError as e:
            error = []
            protected_objects = e.protected_objects
            items = protected_objects.all() if hasattr(protected_objects, 'all') else protected_objects
            for item in items:
                error.append(
                    _('Deleting this item depends on the %(verbose_name)s with ID %(id)s. (%(title)s)')
                    % {
                        'verbose_name': item._meta.verbose_name,
                        'id': str(item.pk),
                        'title': str(item),
                    }
                )
            return Response({'non_field_errors': error}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset_admin(self, request):
        queryset = self.get_queryset()
        return queryset
