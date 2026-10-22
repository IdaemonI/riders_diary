from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)


class Book(models.Model):
    title = models.CharField(max_length=100)

    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="books",
    )

    year = models.DateField("year_of_creation")

    def __str__(self):
        return self.title
