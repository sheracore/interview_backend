from django_filters import compat, filters
from django_filters.rest_framework import DjangoFilterBackend

from .multiplevalues import MultipleValueFilter


class FilterBackend(DjangoFilterBackend):
    def get_filterset_kwargs(self, request, queryset, view):
        kwargs = super().get_filterset_kwargs(request, queryset, view)

        if hasattr(view, 'get_filterset_kwargs'):  # TODO: Maby it doen't need anymore for SKYLOOV
            kwargs.update(view.get_filterset_kwargs())
        return kwargs

    def get_coreschema_field(self, field):
        if isinstance(field, (filters.NumberFilter, filters.NumericRangeFilter, filters.RangeFilter)):
            field_cls = compat.coreschema.Number
        elif isinstance(field, filters.BooleanFilter):
            field_cls = compat.coreschema.Boolean
        elif isinstance(
            field,
            (
                MultipleValueFilter,
                filters.MultipleChoiceFilter,
                filters.ModelMultipleChoiceFilter,
                filters.AllValuesMultipleFilter,
            ),
        ):
            field_cls = compat.coreschema.Array
        elif isinstance(field, filters.OrderingFilter):
            field_cls = compat.coreschema.Object
        else:
            field_cls = compat.coreschema.String

        return field_cls(
            description=field.extra.get("help_text", ""),
        )
