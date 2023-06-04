import django_filters
from django_filters import rest_framework as filters

from .multiplevalues import MultipleValueFilter


class DataModelFilterSet(filters.FilterSet):
    def __init__(self, *args, request_data=None, **kwargs):
        if request_data is None:
            request_data = {}
        request_data.update(kwargs['data'].dict())
        kwargs['data'] = request_data
        super().__init__(*args, **kwargs)

    pks = MultipleValueFilter(
        field_name='pk', lookup_expr='in', help_text={'description': 'Primary Keys', "example": '[1,2,3]'}
    )
    created_at = django_filters.DateTimeFromToRangeFilter(
        help_text={
            'description': 'When created',
            "example": "created_at_after: '2022-12-28T15:33:57.7', created_at_before: '2023-12-28T15:33:57.7'",
        }
    )
    update_at = django_filters.DateTimeFromToRangeFilter(
        help_text={
            'description': 'When updated',
            "example": "update_at_after: '2022-12-28T15:33:57.7', update_at_before: '2023-12-28T15:33:57.7'",
        }
    )
    is_active = django_filters.BooleanFilter(help_text={'description': 'Active status', "example": 'True'})


class UserDataModelFilterSet(DataModelFilterSet):
    user_emails = MultipleValueFilter(
        field_name='user__email',
        help_text={'description': 'Contain emails', "example": "['m.ghaffari662@gmail.com', 'rsabzeh@gmail.com']"},
    )
    user_pks = MultipleValueFilter(
        field_name='user__pk',
        help_text={
            'description': 'User pks',
            "example": "['f22a8d24-6936-46be-b893-9aee198836ed', 'f22a8d24-6936-46be-b893-9aee198836ed']",
        },
    )
    user_is_active = django_filters.BooleanFilter(
        field_name='user__is_active', help_text={'description': 'User active status', "example": 'True'}
    )
    user_is_staff = django_filters.BooleanFilter(
        field_name='user__is_staff', help_text={'description': 'Is user staff?', "example": 'False'}
    )
    user_email = django_filters.CharFilter(
        field_name='user__email',
        lookup_expr='icontains',
        help_text={'description': 'Email', "example": 'm.ghaffari662@gmail.com'},
    )
    user_created_at = django_filters.DateTimeFromToRangeFilter(
        field_name='user__created_at',
        help_text={
            'description': 'When user created',
            "example": "user_created_at_after: '2022-12-28T15:33:57.7', user_created_at_before: '2023-12-28T15:33:57'",
        },
    )
    user_update_at = django_filters.DateTimeFromToRangeFilter(
        field_name='user__update_at',
        help_text={
            'description': 'When user updated',
            "example": "user_update_at_after: '2022-12-28T15:33:57.7', user_update_at_before: '2023-12-28T15:33:57.7'",
        },
    )
