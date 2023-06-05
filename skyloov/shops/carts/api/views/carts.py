from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from skyloov.shops.models import Cart, CartItem
from skyloov.utilities.api.paginations import StandardResultsSetPagination
from skyloov.utilities.api.views import UserDataModelViewSet
from skyloov.utilities.permissions import AllowOwner, AllowStaffOrOwner

from ..filters import CartFilterSet
from ..serializers import CartDetailSerializer, CartSummarySerializer

"""
Cart
"""


class CartViewSet(UserDataModelViewSet):
    queryset = Cart.objects.none()
    model = Cart
    pagination_class = StandardResultsSetPagination
    filterset_class = CartFilterSet
    OrderingFilter = ('status', 'created_at', 'update_at')

    serializers = {
        'default': CartSummarySerializer,
        'retrieve': CartDetailSerializer,
        'create': CartDetailSerializer,
        'update': CartDetailSerializer,
        'update_items': CartDetailSerializer,
        'remove_items': CartDetailSerializer,
    }
    permission_classes_by_action = {
        'default': [AllowOwner],
        'retrieve': [AllowStaffOrOwner],
        'list': [AllowOwner],
        'create': [AllowOwner],
        'update': [AllowOwner],
        'update_items': [AllowOwner],
        'remove_items': [AllowOwner],
    }

    def get_queryset(self):
        user = self.request.user
        queryset = super(CartViewSet, self).get_queryset()
        if self.action == 'list':
            queryset = queryset.filter(user=user)
        return queryset

    @action(methods=['put'], detail=True)
    def update_items(self, request, pk):
        """This action will be used for add cart-items(items) to card and update existing quantities"""
        obj = self.get_object()
        items = request.data.get('items', [])
        for item in items:
            resource_type = item.get('resourcetype', None)
            quantity = item.get('quantity', 1)
            pk = item.get('pk', None)
            if resource_type is None or pk is None:
                continue
            content_type = ContentType.objects.get(model=resource_type.lower())
            (o_item, created) = CartItem.objects.get_or_create(
                user=request.user,
                cart=obj,
                content_type=content_type,
                object_id=pk,
            )
            if quantity == 0:
                o_item.delete()
            else:
                o_item.quantity = quantity
                o_item.save()
        """
        It must be here because item prefetch and foreign key must be reload.
        """
        obj = self.get_object()
        serializer = self.get_serializer(obj, many=False, read_only=True, context={'request': request}).data
        return Response(serializer, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def remove_items(self, request, pk):
        obj = self.get_object()
        items = request.data.get('items', [])
        for item in items:
            resource_type = item.get('resourcetype', None)
            pk = item.get('pk', None)
            if resource_type is None or pk is None:
                continue
            content_type = ContentType.objects.get(model=resource_type.lower())
            CartItem.objects.filter(
                user=request.user,
                cart=obj,
                content_type=content_type,
                object_id=pk,
            ).delete()
        """
        It must be here because item prefetch and foreign key must be reload.
        """
        obj = self.get_object()
        serializer = self.get_serializer(obj, many=False, read_only=True, context={'request': request}).data
        return Response(serializer, status=status.HTTP_200_OK)
