import time
import json
import subprocess


from celery import shared_task
from skyloov.core.files.models import FileModel, FileStatus, FileType
from skyloov.utilities import round_number, logger


@shared_task
def file_model_process(obj_id):
    """File model process via a channel to celery."""
    time.sleep(0.5)
    # DO nothing at this time
    # It's important calculate file size run first of all.
    if (
            FileModel.objects.filter(pk=obj_id, status=FileStatus.RUNNING).exists()
            or FileModel.objects.filter(status=FileStatus.RUNNING).count() > 3
    ):
        return

    obj = FileModel.objects.get(pk=obj_id)
    update_file(obj_id, {'status': FileStatus.RUNNING})

    try:
        calculate_file_size(obj_id)
        calculate_duration(obj_id)
    except:
        logger.exception("exception raise file_model_process", stack_info=True)
        update_file(obj_id, {'status': FileStatus.FAILED})

    obj.refresh_from_db()
    if obj.status == FileStatus.RUNNING:
        update_file(obj_id, {'status': FileStatus.FINISHED})
        

def update_file(obj_id, update_items):
    FileModel.objects.filter(pk=obj_id).update(**update_items)
    return FileModel.objects.get(pk=obj_id)


def calculate_file_size(obj_id):
    obj = FileModel.objects.get(pk=obj_id)
    update_file(obj_id, {'size': obj.file.size})


def calculate_duration(obj_id):
    obj = FileModel.objects.get(pk=obj_id)
    if obj.type == FileType.MOVIE or obj.type == FileType.VOICE:
        try:
            command = "ffprobe -i '{}' -v quiet -print_format json -show_format -hide_banner".format(obj.file.path)
            command_output = subprocess.check_output(
                command,
                shell=True,
                close_fds=True,
            )
            command_output = json.loads(command_output)
            duration = int(round_number(command_output.get('format', {}).get('duration', 0)))
            if obj.duration != duration:
                FileModel.objects.filter(pk=obj_id).update(duration=duration)
        except Exception as e:
            logger.exception("Cant find duration", stack_info=True, extra={'file_id': obj_id})
            update_file(obj_id, {'status': FileStatus.FAILED})
    return 0
