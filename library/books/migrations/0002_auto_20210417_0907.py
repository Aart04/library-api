# Generated by Django 3.2 on 2021-04-17 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='average_rating',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='categories',
            field=models.ManyToManyField(blank=True, null=True, to='books.Category'),
        ),
        migrations.AlterField(
            model_name='book',
            name='ratings_count',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='thumbnail',
            field=models.URLField(blank=True, null=True),
        ),
    ]
