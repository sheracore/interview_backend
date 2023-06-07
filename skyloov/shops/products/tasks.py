import time
from PIL import Image
from io import BytesIO
from celery import shared_task
from django.core.files import File

from skyloov.utilities import logger
from skyloov.core.files.models import FileModel

from .enums import ProductImageSize, ProductImageFormat
from .models import Product


@shared_task
def product_thumbnail_generator(o_id, user_id):
    time.sleep(0.2)
    try:
        obj = Product.objects.get(pk=o_id)
        original_image = obj.image_original
        image = Image.open(original_image.path)
        image.thumbnail((
            ProductImageSize.THUMBNAIL.width,
            ProductImageSize.THUMBNAIL.height
        ), Image.ANTIALIAS)
        temp_image_io = BytesIO()
        image.save(temp_image_io, format=ProductImageFormat.DEFAULT.get_value)
        temp_image_io.seek(0)
        file_object = File(temp_image_io, name=ProductImageSize.THUMBNAIL.name)
        f_id = FileModel.objects.create(
            title=obj.title,
            file=file_object,
            user_id=user_id
        )
        obj.image_thumbnail = f_id
        obj.save()
    except Exception as e:
        logger.error(f"An error occurred while creating thumbnail for product: {e}")

