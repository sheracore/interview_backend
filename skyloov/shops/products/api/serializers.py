from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from skyloov.utilities.api.serializers import DataModelDetailSerializer, DataModelSummarySerializer

from ..models import Product


def _validate_range(min_value, max_value, error_message):
    if min_value and max_value and min_value > max_value:
        raise ValidationError(error_message)


class ProductSummarySerializer(DataModelSummarySerializer):
    class Meta:
        model = Product
        fields = (
            DataModelSummarySerializer.Meta.fields
            + [
                'title',
                'price',
                'quantity',
                'brand',
                'category',
                'rating',
                'image_thumbnail',
                'image_original'
            ]
        )

        read_only_fields = (
            DataModelSummarySerializer.Meta.fields + [
                'rating',
        ]
        )


class ProductDetailSerializer(ProductSummarySerializer, DataModelDetailSerializer):
    class Meta:
        model = Product
        fields = (
            DataModelDetailSerializer.Meta.fields
            + ProductSummarySerializer.Meta.fields
            + []
        )

        read_only_fields = (
            DataModelDetailSerializer.Meta.read_only_fields
            + ProductSummarySerializer.Meta.read_only_fields
            + []
        )


class ProductFilterSerializer(serializers.Serializer):
    category = serializers.CharField(allow_blank=True, required=False)
    brand = serializers.CharField(allow_blank=True, required=False)
    min_price = serializers.DecimalField(max_digits=20, decimal_places=0, required=False)
    max_price = serializers.DecimalField(max_digits=20, decimal_places=0, required=False)
    min_rating = serializers.FloatField(required=False)
    max_rating = serializers.FloatField(required=False)
    min_quantity = serializers.IntegerField(min_value=0, required=False)
    max_quantity = serializers.IntegerField(min_value=0, required=False)
    created_at_after = serializers.DateTimeField(required=False)
    created_at_before = serializers.DateTimeField(required=False)

    class Meta:
        fields = [
                'category',
                'brand',
                'min_price',
                'max_price',
                'min_quantity',
                'max_quantity',
                'created_at_after',
                'created_at_before',
                ]

        read_only_fields = []

    def validate(self, attrs):
        _validate_range(
            attrs.get('min_price'),
            attrs.get('max_price'),
            _("Min price must be less than or equal to max price.")
        )
        _validate_range(
            attrs.get('min_quantity'),
            attrs.get('max_quantity'),
            _("Min quantity must be less than or equal to max quantity.")
        )
        _validate_range(
            attrs.get('min_rating'),
            attrs.get('max_rating'),
            _("Min rating must be less than or equal to max rating.")
        )
        _validate_range(
            attrs.get('created_at_after'),
            attrs.get('created_at_before'),
            _("Created at after must be less than or equal to Created at before.")
        )
        return attrs


