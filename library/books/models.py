from django.db import models
from django.core.exceptions import ValidationError
from datetime import date


class Book(models.Model):
    PARTIAL_YEAR = '%Y'
    PARTIAL_MONTH = '%Y-%m'
    PARTIAL_DAY = '%Y-%m-%d'

    PARTIAL_DATE_TYPES = (
        (PARTIAL_YEAR, 'Year only'),
        (PARTIAL_MONTH, 'Year and month'),
        (PARTIAL_DAY, 'Full year'),
    )

    book_id = models.CharField(max_length=250, primary_key=True)
    title = models.CharField(max_length=250)
    authors = models.ManyToManyField('Author')
    published_date_type = models.CharField(max_length=100, choices=PARTIAL_DATE_TYPES, blank=True, null=True)
    published_date = models.DateField(blank=True, null=True)
    categories = models.ManyToManyField('Category', blank=True)
    average_rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    ratings_count = models.PositiveIntegerField(blank=True, null=True)
    thumbnail = models.URLField(blank=True, null=True)

    def clean(self):
        if self.published_date is not None:
            if self.published_date_type == self.PARTIAL_YEAR:
                self.published_date = date(self.published_date.year, 1, 1)
            elif self.published_date_type == self.PARTIAL_MONTH:
                self.published_date = date(self.published_date.year,
                                           self.published_date.month, 1)
        else:
            raise ValidationError("Please enter date")

    def save(self, *args, **kwargs):
        if self.published_date_type == self.PARTIAL_YEAR:
            self.published_date = date(self.published_date.year, 1, 1)
        elif self.published_date_type == self.PARTIAL_MONTH:
            self.published_date = date(self.published_date.year,
                                       self.published_date.month, 1)
        super(Book, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Author(models.Model):
    fullname = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return self.fullname


class Category(models.Model):
    name = models.CharField(max_length=200, primary_key=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


def partial_str_date_to_date(str_date):
    date_type = None
    date_formatted = None

    split_date = str_date.split("-")

    if len(split_date) == 1:
        date_type = Book.PARTIAL_YEAR
        date_formatted = date(int(split_date[0]), 1, 1)
    elif len(split_date) == 2:
        date_type = Book.PARTIAL_MONTH
        date_formatted = date(int(split_date[0]), int(split_date[1]), 1)
    elif len(split_date) == 3:
        date_type = Book.PARTIAL_MONTH
        date_formatted = date(int(split_date[0]), int(split_date[1]), int(split_date[2]))

    return date_type, date_formatted
