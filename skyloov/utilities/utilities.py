import decimal
import logging


def round_number(value):
    value = decimal.Decimal(value)
    return value.quantize(decimal.Decimal('1.'), rounding=decimal.ROUND_UP)


def get_logger():
    return logging.getLogger(__name__)
