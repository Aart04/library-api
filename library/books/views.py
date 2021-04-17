from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, filters, status
from rest_framework.exceptions import APIException

from .models import Book, Author, Category
from .serializers import BookSerializer
from .services import get_book_data

from datetime import date


class BookDetail(APIView):

    def get_object(self, book_id):
        try:
            return Book.objects.get(book_id=book_id)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, book_id, format=None):
        book = self.get_object(book_id)
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
            try:
                published_date_temp = date(int(published_date_year), 1, 1)
            except ValueError:
                raise APIException(detail="wrong date")

        if published_date_temp is not None:
            queryset = queryset.filter(published_date__year=published_date_temp.year)
        return queryset


class LibrarySave(APIView):

    def post(self, request, format=None):
        q = request.data['q']
        books = get_book_data(q=q)["items"]

        for book in books:
            book_id = book["id"]
            volume_info = book["volumeInfo"]
            title = volume_info["title"]
            volume_info_fields = {"authors": [],
                                  "categories": [],
                                  "averageRating": None,
                                  "ratingsCount": None,
                                  "imageLinks": None
                                  }
            for k, v in volume_info_fields.items():
                if k in volume_info:
                    volume_info_fields[k] = volume_info[k]

            if "publishedDate" in volume_info:
                published_date = volume_info["publishedDate"]
                split_date = published_date.split("-")
                if len(split_date) == 1:
                    published_date_type = Book.PARTIAL_YEAR
                    published_date_formatted = date(int(split_date[0]), 1, 1)
                elif len(split_date) == 2:
                    published_date_type = Book.PARTIAL_MONTH
                    published_date_formatted = date(int(split_date[0]), int(split_date[1]), 1)
                elif len(split_date) == 3:
                    published_date_type = Book.PARTIAL_MONTH
                    published_date_formatted = date(int(split_date[0]), int(split_date[1]), int(split_date[2]))
            else:
                published_date_type = None
                published_date_formatted = None

            if volume_info_fields["imageLinks"] is not None:
                if "thumbnail" in volume_info_fields["imageLinks"]:
                    thumbnail = volume_info["imageLinks"]["thumbnail"]
            else:
                thumbnail = None

            b = Book(book_id=book_id,
                     title=title,
                     published_date_type=published_date_type,
                     published_date=published_date_formatted,
                     average_rating=volume_info_fields["averageRating"],
                     ratings_count=volume_info_fields["ratingsCount"],
                     thumbnail=thumbnail)
            b.save()

            for author_fullname in volume_info_fields["authors"]:
                a = Author(fullname=author_fullname)
                a.save()
                b.authors.add(a)

            for category_name in volume_info_fields["categories"]:
                c = Category(name=category_name)
                c.save()
                b.categories.add(c)

        return Response(status=status.HTTP_201_CREATED)
