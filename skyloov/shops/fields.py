from django.db import models


class PriceField(models.DecimalField):
    def __init__(self, big=False, max_digits=8, decimal_places=0, *args, **kwargs):
        if big:
            max_digits = 20
        super(PriceField, self).__init__(max_digits=max_digits, decimal_places=decimal_places, *args, **kwargs)
