from django.http import HttpResponseNotFound
# from sentry_sdk import capture_message


def page_not_found_view(*args, **kwargs):
    # capture_message("Page not found!", level="error")

    # return any response here, e.g.:
    return HttpResponseNotFound("Not found")
