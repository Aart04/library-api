from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code

    return response