import datetime

from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from .models import Book, Author, Category


class BookViewTest(TestCase):

    def setUp(self):
        n = 10

        # Create n book with different authors and categories
        for i in range(0, n):
            test_author = Author.objects.create(fullname="Test Name_{}".format(i))
            test_author.save()

            test_category = Category.objects.create(name="Test Category_{}".format(i))
            test_category.save()

            test_book = Book.objects.create(
                book_id='BookID_{}'.format(i),
                title='Book Title_{}'.format(i),
                published_date_type=Book.PARTIAL_DAY,
                published_date=datetime.date(2021 - i,
                                             4,
                                             i + 1),
                average_rating=3,
                ratings_count=3,
                thumbnail='https://www.test.com'
            )
            test_book.save()
            test_book.authors.add(test_author)
            test_book.categories.add(test_category)

    def test_detail_info_based_on_book_id(self):
        test_book_id = "BookID_1"
        expected_response_data = {
            "book_id": "BookID_1",
            "title": "Book Title_1",
            "authors": [
                "Test Name_1"
            ],
            "published_date": "2020-04-02",
            "categories": [
                "Test Category_1"
            ],
            "average_rating": "3.0",
            "ratings_count": 3,
            "thumbnail": "https://www.test.com"}

        response = self.client.get('/books/{}'.format(test_book_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response_data)

    def test_detail_404_when_book_with_book_id_not_exists(self):
        test_book_id = "Non_existing"
        response = self.client.get('/books/{}'.format(test_book_id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_books_list_all_books_in_list(self):
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_books_list_filtered_by_published_date(self):
        response = self.client.get('/books/?published_date=2021')
        expected_response_data = [{
            "book_id": "BookID_0",
            "title": "Book Title_0",
            "authors": [
                "Test Name_0"
            ],
            "published_date": "2021-04-01",
            "categories": [
                "Test Category_0"
            ],
            "average_rating": "3.0",
            "ratings_count": 3,
            "thumbnail": "https://www.test.com"}]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response_data)

    def test_books_list_order_by_published_date_asc(self):
        response = self.client.get('/books/?sort=published_date')
        last_year = 0
        for book in response.data:
            current_book_date = datetime.datetime.strptime(book["published_date"], "%Y-%m-%d")
            if last_year == 0:
                last_year = current_book_date.year
            else:
                self.assertTrue(last_year <= current_book_date.year)
                last_year = current_book_date.year
