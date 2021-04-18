import requests

from django.http import Http404

from rest_framework import status
from rest_framework.exceptions import APIException

from .utils import ServiceUnavailable


def get_book_data(q):
    url = "https://www.googleapis.com/books/v1/volumes?q={}".format(q)
    response = requests.get(url=url)
    response_status = response.status_code
    if response_status == status.HTTP_200_OK:
        return response.json()
    elif response_status == status.HTTP_404_NOT_FOUND:
        raise Http404()
    elif response_status == status.HTTP_503_SERVICE_UNAVAILABLE:
        raise ServiceUnavailable
    else:
        raise APIException(status=response_status)

