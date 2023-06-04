from skyloov.utilities.api.views import DataModelViewSet
from skyloov.utilities.api.paginations import StandardResultsSetPagination
from skyloov.utilities.permissions import AllowStaff
from rest_framework.permissions import IsAuthenticated, AllowAny

from ..models import Product
from ..api.serializers import ProductSummarySerializer, ProductDetailSerializer
from .filter import ProductFilterSet


class ProductViewSet(DataModelViewSet):
    queryset = Product.objects.none()
    model = Product
    filterset_class = ProductFilterSet
    pagination_class = StandardResultsSetPagination
    OrderingFilter = (
        'title',
        'price_fabric',
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
    }
    permission_classes_by_action = {
        'default': [AllowStaff],
        'retrieve': [IsAuthenticated],
        'list': [IsAuthenticated],
        'create': [
            AllowStaff,
        ],
        'update': [
            AllowStaff,
        ],
    }
