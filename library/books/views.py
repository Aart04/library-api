from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, filters, status
from rest_framework.exceptions import APIException

from .models import Book, Author, Category, partial_str_date_to_date
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
        response = get_book_data(q=q)

        if "items" in response:
            books = response["items"]
        else:
            raise Http404

        for book in books:
            book_id = book["id"]
            volume_info = book["volumeInfo"]
            title = volume_info["title"]
            volume_info_fields = {"authors": [],
                                  "categories": [],
                                  "publishedDate": None,
                                  "averageRating": None,
                                  "ratingsCount": None,
                                  "imageLinks": None
                                  }
            published_date_type = None
            thumbnail = None
            for k, v in volume_info_fields.items():
                if k in volume_info:
                    if k == "publishedDate":
                        published_date_type, volume_info_fields[k] = partial_str_date_to_date(volume_info[k])
                    elif k == "imageLinks":
                        if "thumbnail" in volume_info["imageLinks"]:
                            thumbnail = volume_info["imageLinks"]["thumbnail"]
                    else:
                        volume_info_fields[k] = volume_info[k]

            b = Book(book_id=book_id,
                     title=title,
                     published_date_type=published_date_type,
                     published_date=volume_info_fields["publishedDate"],
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
