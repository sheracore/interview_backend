from django.core.validators import MinLengthValidator
from django.db import models
from skyloov.utilities.db.models import (
    DataModel,
    DataModelManager,
    DataModelQuerySet
)

from django.utils.translation import gettext_lazy as _

from skyloov.shops.fields import PriceField


class Brand(models.TextChoices):
    LENNAR = 'lennar', _('Lennar')
    DR_HORTON = 'dr_horton', _('DR Horton')
    PULTE_HOEMS = 'pulte_homes', _('Pulte Homes')
    TOLL_BROTHERS = 'toll_brothers', _('Toll Brothers')
    KB_HOME = 'kb_home', _('KB Home')


class Category(models.TextChoices):
    SINGLE_FAMILY = 'single_family', _('Single_family')
    CONDOMINIUMS = 'condominiums', _('Condominiums')
    TOWNHOUSES = 'townhouses', _('Townhouses')
    DUPLEXES = 'duplexes', _('Duplexes')
    APARTMENTS = 'apartments', _('Apartments')
    VILLAS = 'villas', _('Villas')
    BUNGALOWS = 'bungalows', _('Bungalows')
    MANSIONS = 'mansions', _('Mansions')
    TINY = 'tiny', _('Tiny')
    HOUSES = 'houses', _('Houses')
    MOBILE = 'mobile', _('Mobile')
    HOMES = 'homes', _('Homes')


class ProductQuerySet(DataModelQuerySet):
    pass


class ProductManager(DataModelManager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)


class Product(DataModel):
    title = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)],
        verbose_name=_('Title'),
    )
    price = PriceField(
        big=True,
        verbose_name=_('Price Fabric'),
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_('Discount Price'),
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

    objects = ProductManager()

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
