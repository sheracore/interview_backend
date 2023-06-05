from django_filters import rest_framework as filters

from skyloov.utilities.api.filters import UserDataModelFilterSet


class CartFilterSet(UserDataModelFilterSet):
    title = filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        help_text={'description': 'Title', "example": "basket2"},
    )
