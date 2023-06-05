from django.contrib.contenttypes.models import ContentType


def get_content_type_dictionary():
    content_type_dictionary = dict()
    try:
        def ignore_it(app):
            blacklist = [
                'admin',
                'auth',
                'django',
                'contenttypes',
                'sessions',
                'otp',
                'device',
                'push',
                'content',
                'azbankgateways',
                'bank',
            ]
            for item in blacklist:
                if app.app_label.find(item) >= 0:
                    return True
                if app.model.find(item) >= 0:
                    return True
            return False

        for item in ContentType.objects.all():
            if ignore_it(item) or not item.model_class():
                continue
            content_type_dictionary[item.model_class().__name__] = item.pk
        return content_type_dictionary
    except Exception:
        pass
