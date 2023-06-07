from django.utils.dateparse import parse_datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from skyloov.utilities.api.views import UserDataModelViewSet
from skyloov.utilities.api.paginations import StandardResultsSetPagination
from skyloov.utilities.permissions import AllowStaff

from ..models import Product
from ..api.serializers import (
    ProductSummarySerializer,
    ProductDetailSerializer,
    ProductImageUploadSerializer,
    ProductFilterSerializer,
)
from .filter import ProductFilterSet
from ..utils import upload_image


class ProductViewSet(UserDataModelViewSet):
    queryset = Product.objects.none()
    model = Product
    filterset_class = ProductFilterSet
    pagination_class = StandardResultsSetPagination
    OrderingFilter = (
        'title',
        'price',
        'quantity',
        'brand',
        'category',
        'created_at',
        'update_at',
    )

    serializers = {
        'default': ProductSummarySerializer,
        'retrieve': ProductDetailSerializer,
        'create': ProductDetailSerializer,
        'update': ProductDetailSerializer,
        'search': ProductFilterSerializer,
        'update_image': ProductImageUploadSerializer,
    }
    permission_classes_by_action = {
        'default': [AllowStaff],
        'retrieve': [IsAuthenticated],
        'list': [IsAuthenticated],
        'search': [
            IsAuthenticated
        ],
        'create': [
            AllowStaff,
        ],
        'update': [
            AllowStaff,
        ],
        'update_image': [
            AllowStaff
        ]
    }

    @action(methods=['POST'], detail=False)
    def search(self, request):
        data = request.data
        if data:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
        queryset = self.get_queryset()
        filters = {
            'category__icontains': data.get('category'),
            'brand__icontains': data.get('brand'),
            'price__gte': data.get('min_price'),
            'price__lte': data.get('max_price'),
            'quantity__gte': data.get('min_quantity'),
            'quantity__lte': data.get('max_quantity'),
            'rating__gte': data.get('min_rating'),
            'rating__lte': data.get('max_rating'),
            'created_at__gte': parse_datetime(data.get('created_at_after')) if data.get('created_at_after') else None,
            'created_at__lte': parse_datetime(data.get('created_at_before')) if data.get('created_at_before') else None
        }

        queryset = queryset.filter(**{k: v for k, v in filters.items() if v is not None})
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = ProductSummarySerializer(paginated_queryset, context={'request': request}, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['POST'], detail=True)
    def update_image(self, request, pk):
        user_obj = request.user
        product_obj = self.get_object()
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        image = request.FILES['image']
        upload_image(image, product_obj, user_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True)
    def rate(self, request, pk):
        # TODO: Implement rating Here, rate products by users and calculate average if product rating
        return Response({}, status=status.HTTP_200_OK)
