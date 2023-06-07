import magic
import threading

from skyloov.core.files.models import FileModel
from django.core.files.uploadedfile import TemporaryUploadedFile


def upload_image(in_memory_image, product_obj, user_obj):

    def worker(file_name, mime_type, file_size, file_data):
        tf = TemporaryUploadedFile(file_name, mime_type, file_size, None)
        tf.write(file_data)
        tf.seek(0)

        f_obj = FileModel.objects.create(
            title=product_obj.title,
            file=tf,
            user=user_obj
        )
        tf.close()
        product_obj.image_thumbnail = None
        product_obj.image_original = f_obj
        product_obj.save()

    file_name = in_memory_image.name
    mime_type = magic.from_buffer(in_memory_image.read(20480), mime=True)
    in_memory_image.seek(0)
    file_size = in_memory_image.size
    file_data = in_memory_image.read()

    thread = threading.Thread(target=worker, args=(file_name, mime_type, file_size, file_data))
    thread.start()
