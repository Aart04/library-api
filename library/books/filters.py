from django_filters import rest_framework as filters
from .models import Book


class AuthorFilter(filters.FilterSet):
    author = filters.Filter(field_name="authors__fullname", lookup_expr='in')

    class Meta:
        model = Book
        fields = ['authors__fullname']
