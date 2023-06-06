from django.core.exceptions import ValidationError
from django.db.models import ForeignKey
from django.utils.translation import gettext_lazy as _


class FileField(ForeignKey):
    def __init__(self, to=None, allow_type=[], **kwargs):
        kwargs['to'] = 'files.FileModel'
        self.allow_type = allow_type
        super(FileField, self).__init__(**kwargs)

    def validate(self, value, model_instance):
        from skyloov.core.files.models import FileModel

        if len(self.allow_type) > 0:
            obj = FileModel.objects.get(pk=value)
            is_find = False
            for item in self.allow_type:
                if obj.type == item:
                    is_find = True
                    break
            if not is_find:
                raise ValidationError(
                    [
                        _('You must choose valid type %(type)s.')
                        % {
                            'type': ', '.join(x.label for x in self.allow_type),
                        }
                    ]
                )

            super(FileField, self).validate(value, model_instance)
