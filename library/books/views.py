from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import filters
from rest_framework import status

from .models import Book
from .serializers import BookSerializer
from .services import get_book_data

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

        if authors:
            queryset = queryset.filter(authors__fullname__in=authors).distinct()

        published_date_temp = None
        if published_date_year is not None:
            published_date_temp = date(int(published_date_year), 1, 1)
        if published_date_temp is not None:
            queryset = queryset.filter(published_date__year=published_date_temp.year)
        return queryset


class LibrarySave(APIView):

    def post(self, request, format=None):
        q = request.data['q']
        books = get_book_data(q=q)["items"]

        for book in books:
            id = book["id"]
            volume_info = book["volumeInfo"]
            title = volume_info["title"]
            authors = volume_info["authors"]
            published_date = volume_info["publishedDate"]
            if "categories" in volume_info:
                categories = volume_info["categories"]
            else:
                categories = []
            if "averageRating" in volume_info:
                average_rating = volume_info["averageRating"]
            else:
                average_rating = None
            if "ratingsCount" in volume_info:
                ratings_count = volume_info["ratingsCount"]
            else:
                ratings_count = None
            if "imageLinks" in volume_info:
                imageLinks = volume_info["imageLinks"]
                if "thumbnail" in imageLinks:
                    thumbnail = volume_info["imageLinks"]["thumbnail"]
                else:
                    thumbnail = None
        return Response(data=books, status=status.HTTP_201_CREATED)
