import enum
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

key_type_error_message = "This key: '%(key)s', does not exists"


class ProductImageSize(enum.Enum):
    """
    Enum for product images
    """

    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    ORIGINAL = 'ORIGINAL'
    THUMBNAIL = 'THUMBNAIL'

    @property
    def width(self) -> int:
        if self.name == self.ORIGINAL.name:
            return 1024
        elif self.name == self.THUMBNAIL.name:
            return 512
        elif self.name == self.SMALL.name:
            return 256
        elif self.name == self.MEDIUM.name:
            return 512
        elif self.name == self.HIGH.name:
            return 2048
        else:
            raise ValidationError({"key": [_(key_type_error_message) % {'key': self.name}]})

    @property
    def height(self) -> int:
        if self.name == self.ORIGINAL.name:
            return 1024
        elif self.name == self.THUMBNAIL.name:
            return 512
        elif self.name == self.SMALL.name:
            return 256
        elif self.name == self.MEDIUM.name:
            return 512
        elif self.name == self.HIGH.name:
            return 2048
        else:
            raise ValidationError({"key": [_(key_type_error_message) % {'key': self.name}]})

    @property
    def get_size(self) -> int:
        if self.name == self.SMALL.name:
            return 20 * 1024 * 1024
        elif self.name == self.MEDIUM.name:
            return 40 * 1024 * 1024
        elif self.name == self.HIGH.name:
            return 80 * 1024 * 1024
        elif self.name == self.THUMBNAIL.name:
            return 8 * 1024 * 1024
        elif self.name == self.ORIGINAL.name:
            return 40 * 1024 * 1024
        else:
            raise ValidationError({"key": [_(key_type_error_message) % {'key': self.name}]})


class ProductImageFormat(enum.Enum):
    DEFAULT = "DEFAULT"

    @property
    def get_value(self) -> str:
        if self.name == self.DEFAULT.name:
            return 'JPEG'
