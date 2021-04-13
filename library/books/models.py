from django.db import models

from partial_date import PartialDateField


class Book(models.Model):
    title = models.CharField(max_length=250)
    authors = models.ManyToManyField('Author')
    published_date = PartialDateField()
    categories = models.ManyToManyField('Category')
    average_rating = models.DecimalField(max_digits=2, decimal_places=1)
    ratings_count = models.PositiveIntegerField()
    thumbnail = models.URLField()

    def __str__(self):
        return self.title


class Author(models.Model):
    fullname = models.CharField(max_length=200)

    def __str__(self):
        return self.fullname


class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name
