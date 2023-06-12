import magic
import mimetypes
import random
import blurhash
import json
import subprocess

from os import path
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from skyloov.utilities.languages import replace_non_english_characters


"""
FileValidator
"""


def validate_file(value):
    (file_type, mime) = detect_type(value)
    if not file_type:
        raise ValidationError(
            _('Type %(type)s doesnt support.')
            % {
                'type': mime,
            }
        )


"""
Upload path
"""


def get_document_path(instance, filename):
    from .models import FileType

    if instance.type == FileType.APK:
        guess_extension = 'apk'
    elif instance.type == FileType.IPA:
        guess_extension = 'ipa'
    else:
        mime = get_mime(instance.file)
        guess_extension = mimetypes.guess_extension(mime)
        if guess_extension:
            guess_extension = guess_extension[1:]
        else:
            guess_extension = filename.split(".")[-1][-5:]
    name = '{0}-{1}-{2}.{3}'.format(
        replace_non_english_characters(filename.split(".")[0][:14]),
        now().strftime('%y-%m-%d-%H-%M-%S'),
        random.randint(0, 10000),
        guess_extension,
    )
    return name


def get_mime(file_field):
    file_field.seek(0)
    mime = magic.from_buffer(file_field.read(20480), mime=True)
    return mime


"""
blur hash 
"""


def blur_hash_calculate(file_path):
    if not path.isfile(file_path):
        return None
    try:
        blur_hash = blurhash.encode(file_path, x_components=4, y_components=3)
    except:
        return None
    return blur_hash


"""
detect type
"""


def detect_by_readable_description(readable_description):
    from .models import FileType

    readable_description = readable_description.lower()

    if readable_description.find('jpeg') != -1 or readable_description.find('png') != -1:
        return FileType.IMAGE

    elif readable_description.find('audio') != -1:
        return FileType.VOICE

    elif readable_description.find('mpeg') != -1:
        return FileType.MOVIE

    return None


def detect_mime_type(mime):
    from .models import FileType

    mime = mime.lower() if mime else mime
    types_map = {
        FileType.IMAGE: [
            'image/png',
            'image/jpeg',
            'image/jpg',
        ],
        FileType.MOVIE: [
            'video/mpeg',
            'video/mp4',
            'video/x-matroska',
        ],
        FileType.VOICE: [
            'audio/mpeg',
            'application/ogg',
        ],
        FileType.PDF: ['application/pdf'],
        FileType.TEXT: ['text/plain'],
        FileType.CSS: [
            'text/css',
        ],
        FileType.SVG: [
            'image/svg+xml',
        ],
        FileType.JSON: [
            'application/json',
        ],
        FileType.COMPRESS: [
            'application/zip',
        ],
        FileType.IPA: [
            'application/x-ios-app',
        ],
        FileType.SPREADSHEET: [
            'text/csv',
        ],
    }

    for key in types_map:
        for value in types_map[key]:
            if mime == value:
                return key
    return None


def detect_type(file_field):
    mime = get_mime(file_field)
    file_type = detect_mime_type(mime)
    if not file_type:
        file_type = detect_by_readable_description(mime)
        if not file_type:
            try:
                file_path = file_field.file.temporary_file_path()
            except:
                file_path = file_field.path
            file_type = detect_by_ffmpeg(file_path)

    file_type, mime = handle_plain_text_file_type(file_field, file_type, mime)
    file_type, mime = handle_plain_android_compress_file_type(file_field, file_type, mime)
    return file_type, mime


def detect_by_ffmpeg(file_path):
    try:
        command = "ffprobe -i '{}' -v quiet -print_format json -show_format -hide_banner -show_streams".format(
            file_path
        )
        command_output = subprocess.check_output(
            command,
            shell=True,
            close_fds=True,
        )
        command_output = json.loads(command_output)
        mime = command_output.get('format', {}).get('format_long_name', '')
        file_type = detect_by_readable_description(mime.lower())
        if file_type:
            return file_type
        streams = command_output.get('streams', [])
        for stream in streams:
            mime = stream.get('codec_long_name', '')
            file_type = detect_by_readable_description(mime.lower())
            if file_type:
                return file_type
    except Exception:
        pass
    return None


def handle_plain_text_file_type(file_field, file_type, mime):
    from .models import FileType

    if file_type != FileType.TEXT:
        return file_type, mime

    mime_guest = mimetypes.guess_type(file_field.path)[0]
    file_type_guest = detect_mime_type(mime_guest)
    if file_type_guest and mime_guest:
        return file_type_guest, mime_guest
    return file_type, mime


def handle_plain_android_compress_file_type(file_field, file_type, mime):
    from .models import FileType

    if file_type != FileType.COMPRESS:
        return file_type, mime

    extension = str(file_field).split(".")[-1].lower()
    if extension == 'apk':
        file_type = FileType.APK
    elif extension == 'ipa':
        file_type = FileType.IPA
    return file_type, mime
