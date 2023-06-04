from django.core.exceptions import ValidationError
from django.forms.fields import MultipleChoiceField
from django_filters.filters import Filter


class MultipleValueField(MultipleChoiceField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, value):
        """Validate that the input is a list or tuple."""
        if self.required and not value:
            raise ValidationError(self.error_messages['required'], code='required')

    # Override clean method to detect and convert MultipleChoiceField fields from query params
    def clean(self, value):
        if value is not None:
            value = [item.strip() for item in value.split(",")]
        return super(MultipleValueField, self).clean(value)


class MultipleValueFilter(Filter):
    field_class = MultipleValueField

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('lookup_expr', 'in')
        super().__init__(*args, **kwargs)
