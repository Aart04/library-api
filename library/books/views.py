from django.shortcuts import render
from django.http import Http404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import filters

from .models import Book
from .serializers import BookSerializer

from datetime import date


class BookDetail(APIView):

    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['published_date']


    def get_queryset(self):
        queryset = Book.objects.all()
        published_date_year = self.request.query_params.get('published_date')
        authors = self.request.query_params.getlist('author')

        if authors is not None:
            queryset = queryset.filter(authors__fullname__in=authors).distinct()

        published_date_temp = None
        if published_date_year is not None:
            published_date_temp = date(int(published_date_year), 1, 1)
        if published_date_temp is not None:
            queryset = queryset.filter(published_date__year=published_date_temp.year)
        return queryset


