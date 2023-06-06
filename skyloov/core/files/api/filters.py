from django_filters import rest_framework as filters

from skyloov.utilities.api.filters import UserDataModelFilterSet

from ..models import FileStatus, FileType


class FileFilterSet(UserDataModelFilterSet):
    title = filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        help_text={'description': 'search in titles'},
    )
    size = filters.RangeFilter(
        field_name='size',
        help_text={
            'description': 'Size of files',
            "example": "size_max: 100000, size_min:600000",
        },
    )
    type = filters.ChoiceFilter(
        choices=FileType.choices,
        help_text={
            'description': 'Type of files',
            "example": "type: 2",
        },
    )
    status = filters.ChoiceFilter(
        choices=FileStatus.choices,
        help_text={
            'description': 'Status of files',
            "example": "status: 3",
        },
    )
