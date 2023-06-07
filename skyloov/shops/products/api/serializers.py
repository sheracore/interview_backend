from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from skyloov.utilities.api.serializers import UserDataModelDetailSerializer, UserDataModelSummarySerializer
from ..enums import ProductImageSize

from ..models import Product


def _validate_range(min_value, max_value, error_message):
    if min_value and max_value and min_value > max_value:
        raise ValidationError(error_message)


class ProductSummarySerializer(UserDataModelSummarySerializer):
    class Meta:
        model = Product
        fields = (
            UserDataModelSummarySerializer.Meta.fields
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
            UserDataModelSummarySerializer.Meta.fields + [
                'rating',
        ]
        )


class ProductDetailSerializer(ProductSummarySerializer, UserDataModelDetailSerializer):
    class Meta:
        model = Product
        fields = (
            UserDataModelDetailSerializer.Meta.fields
            + ProductSummarySerializer.Meta.fields
            + []
        )

        read_only_fields = (
            UserDataModelDetailSerializer.Meta.read_only_fields
            + ProductSummarySerializer.Meta.read_only_fields
            + []
        )


class ProductImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True, write_only=True)

    class Meta:
        model = Product
        fields = [
                'image'
            ]

        read_only_fields = []

    def validate_image(self, image):
        max_allow_upload_size = ProductImageSize.SMALL.get_size
        file_size = image.size
        size_error = _('Size %(size)s doesnt support.') % {
            'size': file_size,
        }
        if file_size > max_allow_upload_size:
            raise ValidationError([size_error])


#TODO: just for skyloov requirement
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


