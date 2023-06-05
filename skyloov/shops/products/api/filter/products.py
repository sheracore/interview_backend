from django_filters import rest_framework as filters

from skyloov.utilities.api.filters import (
    MultipleValueFilter,
    DataModelFilterSet,
)


class ProductFilterSet(DataModelFilterSet):
    title = filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        help_text={'description': 'Title', "example": "villa123"},
    )
    quantity = filters.RangeFilter(
        field_name='quantity',
        help_text={
            'description': 'Quantity range .',
            "example": "quantity_min:10, quantity_max:100",
        },
    )
    rating = filters.RangeFilter(
        field_name='rating',
        help_text={
            'description': 'Rating range .',
            "example": "rating_min:1, rating_max:5",
        },
    )
    price = filters.RangeFilter(
        field_name='price',
        help_text={
            'description': 'Fabric price range .',
            "example": "price_max:2500000, price_min:150000",
        },
    )
    brand = MultipleValueFilter(
        field_name='brand', help_text={'description': 'Brand', "example": "POST-> ['lennar', 'pulte_homes'] query_params-> lennar,pulte_homes"}
    )
    category = MultipleValueFilter(
        field_name='category', help_text={'description': 'First names', "example": "POST-> ['single_family', 'bungalows'] query_params-> single_family,bungalows"}
    )

