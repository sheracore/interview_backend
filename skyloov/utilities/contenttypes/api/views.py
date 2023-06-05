from rest_framework.decorators import api_view
from rest_framework.response import Response

from skyloov.utilities.contenttypes import get_content_type_dictionary


@api_view()
def content_type_view(request):
    return Response(
        {
            **get_content_type_dictionary(),
        }
    )
