from django.contrib.contenttypes.models import ContentType

from skyloov.utilities.imports.imports import import_attribute


def get_summary_serializer_from_object(obj):
    c_obj = ContentType.objects.get_for_model(obj)
    return get_summary_serializer_from_content_type(c_obj)


def get_summary_serializer_from_content_type(c_obj):
    app_label, model_name = _get_app_detail(c_obj)
    serializer = import_attribute('skyloov.api.serializers', '{}SummarySerializer'.format(model_name))
    return serializer


def _get_app_detail(c_obj):
    app_label = c_obj.app_label
    model_name = c_obj.model_class().__name__
    return (app_label, model_name)
