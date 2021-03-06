# Generated by Django 3.2 on 2021-04-17 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='published_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='published_date_type',
            field=models.CharField(blank=True, choices=[('%Y', 'Year only'), ('%Y-%m', 'Year and month'), ('%Y-%m-%d', 'Full year')], max_length=100, null=True),
        ),
    ]
