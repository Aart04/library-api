from rest_framework import serializers

from .models import Book, Author, Category


class AuthorSerializer(serializers.RelatedField):

    def to_representation(self, value):
        return value.fullname

    class Meta:
        model = Author


class CategorySerializer(serializers.RelatedField):

    def to_representation(self, value):
        return value.name

    class Meta:
        model = Category


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(read_only=True, many=True)
    categories = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = Book
        fields = ['title', 'authors', 'published_date',
                  'categories', 'average_rating', 'ratings_count', 'thumbnail']
