from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse

from rest_framework.test import APIClient, APITestCase
from rest_framework_jwt.settings import api_settings
from rest_framework import status

from ..models import Product, Category, Brand
from ..api.serializers import ProductSummarySerializer

User = get_user_model()

PRODUCT_URL = reverse('product-list')
PRODUCT_SEARCH_URL = reverse('product-search')


def _client_result(res):
    return res.data['results'] if 'results' in res.data else res.data


class ProductTest(APITestCase):
    test_settings = 'DJANGO_PROJECT.test_settings'

    def setUp(self) -> None:
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpassword')
        self.user_staff = User.objects.create_user(
            email='testuserstaff@gmail.com',
            password='testpasswordstaff',
            is_staff=True
        )

    def authenticate_client(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.client.force_authenticate(user=self.user_staff)

    def test_protected_endpoint(self):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(self.user)
        token = jwt_encode_handler(payload)

        self.headers = {"HTTP_AUTHORIZATION": f"{settings.JWT_AUTH.get('JWT_AUTH_HEADER_PREFIX')} {token}"}
        response = self.client.get(PRODUCT_URL, **self.headers)

        self.assertEqual(response.status_code, 200)

    def test_retrieve_product(self):
        """Test retrieving product"""
        Product.objects.create(
            user=self.user,
            title='test1',
            price=50000,
            quantity=10,
            brand=Brand.ASUS,
            category=Category.LAPTOP,
        )
        self.authenticate_client()
        res = self.client.get(PRODUCT_URL)
        product = Product.objects.all().order_by('-title')
        serializer = ProductSummarySerializer(product, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(_client_result(res), serializer.data)

    def test_search_qeury_params_product(self):
        """Test search by query params product"""
        Product.objects.create(
            user=self.user,
            title='phone',
            price=500,
            quantity=1,
            brand=Brand.SAMSUNG,
            category=Category.SMARTWATCH,
        )
        Product.objects.create(
            user=self.user,
            title='smartphone',
            price=1000,
            quantity=2,
            brand=Brand.APPLE,
            category=Category.SMARTWATCH,
        )
        self.authenticate_client()
        res_1 = self.client.get(PRODUCT_URL, {'title': 'phone'})
        res_2 = self.client.get(PRODUCT_URL, {'title': 'smart'})
        res_3 = self.client.get(PRODUCT_URL, {'brand': Brand.SAMSUNG.name.lower()})
        res_4 = self.client.get(PRODUCT_URL, {'price_min': 600})
        res_5 = self.client.get(PRODUCT_URL, {'quantity_max': 3})
        self.assertEqual(len(_client_result(res_1)), 2)
        self.assertEqual(len(_client_result(res_2)), 1)
        self.assertEqual(len(_client_result(res_3)), 1)
        self.assertEqual(len(_client_result(res_4)), 1)
        self.assertEqual(len(_client_result(res_5)), 2)

    def test_search_action_view_product(self):
        """Test search by search action view product"""

        Product.objects.create(
            user=self.user,
            title='tech_phone',
            price=20000,
            quantity=15,
            brand=Brand.GOOGLE,
            category=Category.SMARTPHONE,
        )
        Product.objects.create(
            user=self.user,
            title='tech_devices',
            price=1500,
            quantity=20,
            brand=Brand.MICROSOFT,
            category=Category.SMART_SPEAKER,
        )
        self.authenticate_client()
        res_1 = self.client.post(PRODUCT_SEARCH_URL, {'title': 'tech_'})
        res_2 = self.client.post(PRODUCT_SEARCH_URL, {'brand': Brand.MICROSOFT.name.lower()})
        res_3 = self.client.post(PRODUCT_SEARCH_URL, {'category': Category.SMARTWATCH.name.lower()})
        res_4 = self.client.post(PRODUCT_SEARCH_URL, {'min_price': 500})
        res_5 = self.client.post(PRODUCT_SEARCH_URL, {'max_price': 100000})
        res_6 = self.client.post(PRODUCT_SEARCH_URL, {'min_quantity': 16})
        self.assertEqual(len(_client_result(res_1)), 2)
        self.assertEqual(len(_client_result(res_2)), 1)
        self.assertEqual(len(_client_result(res_3)), 0)
        self.assertEqual(len(_client_result(res_4)), 2)
        self.assertEqual(len(_client_result(res_5)), 2)
        self.assertEqual(len(_client_result(res_6)), 1)

    def test_create_product(self):
        """Test create product"""

        payload1 = {
            "user": self.user,
            "title": 'phone',
            "price": 500,
            "quantity": 15,
            "brand": Brand.APPLE,
            "category": Category.SMARTWATCH
        }
        payload2 = {
            "user": self.user,
            "title": 'laptop',
            "price": 2000,
            "quantity": 5,
            "brand": Brand.ASUS,
            "category": Category.LAPTOP
        }
        self.authenticate_client()
        res_1 = self.client.post(PRODUCT_URL, payload1)
        res_2 = self.client.post(PRODUCT_URL, payload2)
        self.assertEqual(res_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_2.status_code, status.HTTP_201_CREATED)

        products = Product.objects.all()
        self.assertEqual(len(products), 2)
