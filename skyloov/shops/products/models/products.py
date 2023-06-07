from django.db import models
from django.db.models.signals import post_save

from skyloov.utilities.db.models import (
    UserDataModel,
    UserDataModelManager,
    UserDataModelQuerySet
)

from django.utils.translation import gettext_lazy as _
from django.core.validators import (
    MinLengthValidator,
    MinValueValidator,
    MaxValueValidator
)
from skyloov.utilities.db.fields import FileField
from skyloov.core.files.models import FileType
from skyloov.shops.fields import PriceField


class Brand(models.TextChoices):
    APPLE = 'apple', _('Apple')
    SAMSUNG = 'samsung', _('Samsung')
    ASUS = 'asus', _('Asus')
    MICROSOFT = 'microsoft', _('Microsoft')
    GOOGLE = 'google', _('Google')


class Category(models.TextChoices):
    SMARTPHONE = 'smartphone', _('Smartphone')
    LAPTOP = 'laptop', _('Laptop')
    SMARTWATCH = 'smartwatch', _('Smartwatch')
    TABLET = 'tablet', _('Tablet')
    SMART_SPEAKER = 'smart_speaker', _('Smart Speaker')


class ProductQuerySet(UserDataModelQuerySet):
    pass


class ProductManager(UserDataModelManager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)


class Product(UserDataModel):
    title = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)],
        verbose_name=_('Title'),
    )
    price = PriceField(
        big=True,
        verbose_name=_('Price'),
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_('quantity'),
    )
    brand = models.CharField(
        max_length=100,
        blank=False,
        choices=Brand.choices,
        verbose_name=_('Brand'),
    )
    category = models.CharField(
        max_length=100,
        blank=False,
        choices=Category.choices,
        verbose_name=_('Category'),
    )
    # New field with minimum and maximum values for SKYLOOV requirement number 4
    rating = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)]
    )
    image_thumbnail = FileField(
        on_delete=models.SET_NULL,
        related_name='product_image_thumbnail',
        null=True,
        blank=True,
        allow_type=[FileType.IMAGE],
        verbose_name=_('Image Thumbnail'),
    )
    image_original = FileField(
        on_delete=models.SET_NULL,
        related_name='product_image_original',
        null=True,
        blank=True,
        allow_type=[FileType.IMAGE],
        verbose_name=_('Image Original'),
    )

    objects = ProductManager()

    class Meta:
        ordering = ['-id']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


def post_save_product_receiver(sender, instance, created, *args, **kwargs):
    from ..tasks import product_thumbnail_generator

    if instance.image_original and not instance.image_thumbnail:
        product_thumbnail_generator.delay(instance.pk, instance.user.pk) #TODO: should add .delay


post_save.connect(post_save_product_receiver, sender=Product)