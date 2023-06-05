from rest_framework import serializers

from skyloov.utilities.api.serializers import UserDataModelDetailSerializer, UserDataModelSummarySerializer
from skyloov.utilities.api.utils import get_summary_serializer_from_object

from ...models import CartItem


class CartItemSummarySerializer(UserDataModelSummarySerializer):
    content = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = (
            UserDataModelSummarySerializer.Meta.fields
            + [
                'price',
                'quantity',
                'content_type',
                'object_id',
                'content'
            ]
        )

        read_only_fields = (
            UserDataModelSummarySerializer.Meta.fields + [
                'price',
                'quantity',
                'content_type',
                'object_id'
                'content'
            ]
        )

    def get_content(self, obj):
        item = obj.content_object
        serializer = get_summary_serializer_from_object(item)
        return serializer(item, many=False, read_only=True, context=self.context).data


class CartItemDetailSerializer(CartItemSummarySerializer, UserDataModelDetailSerializer):
    class Meta:
        model = CartItem
        fields = (
            UserDataModelDetailSerializer.Meta.fields
            + CartItemSummarySerializer.Meta.fields
            + []
        )

        read_only_fields = (
            UserDataModelDetailSerializer.Meta.read_only_fields
            + CartItemSummarySerializer.Meta.read_only_fields
            + []
        )
