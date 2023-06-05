from rest_framework import serializers
from skyloov.utilities.api.serializers import UserDataModelDetailSerializer, UserDataModelSummarySerializer

from .cartitems import CartItemSummarySerializer
from ...models import Cart


class CartSummarySerializer(UserDataModelSummarySerializer):
    class Meta:
        model = Cart
        fields = (
            UserDataModelSummarySerializer.Meta.fields
            + [
                'title',
                'total_price'
            ]
        )

        read_only_fields = (
            UserDataModelSummarySerializer.Meta.fields + [
                'total_price'
        ]
        )


class CartDetailSerializer(CartSummarySerializer, UserDataModelDetailSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = (
            UserDataModelDetailSerializer.Meta.fields
            + CartSummarySerializer.Meta.fields
            + [
                'items'
            ]
        )

        read_only_fields = (
            UserDataModelDetailSerializer.Meta.read_only_fields
            + CartSummarySerializer.Meta.read_only_fields
            + [
                'items'
            ]
        )

    def get_items(self, obj):
        return CartItemSummarySerializer(obj.items.all(), many=True, read_only=True, context=self.context).data