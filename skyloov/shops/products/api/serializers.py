from skyloov.utilities.api.serializers import DataModelDetailSerializer, DataModelSummarySerializer
from ..models import Product


class ProductSummarySerializer(DataModelSummarySerializer):
    class Meta:
        model = Product
        fields = (
            DataModelSummarySerializer.Meta.fields
            + [
                'title',
                'price_fabric',
                'quantity',
                'brand',
                'category',
            ]
        )

        read_only_fields = (
            DataModelSummarySerializer.Meta.fields + []
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

