from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    birth_data = models.DateField(
        blank=True,
        null=True,
    )


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    isbn = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
    )

    authors = models.ManyToManyField(
        Author,
        related_name="books",
    )

    categories = models.ManyToManyField(
        Category,
        related_name="books",
    )

    publication_year = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    pages = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    cover = models.ImageField(
        upload_to="book_covers",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class UserBook(models.Model):

    class ReadingStatus(models.TextChoices):
        WANT_TO_READ = "want", "Want to read"
        READING = "reading", "Reading"
        READ = "read", "Read"
        PAUSED = "paused", "Paused"
        DROPPED = "dropped", "Dropped"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="readers",
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="library_books",
    )

    status = models.CharField(
        max_length=20,
        choices=ReadingStatus.choices,
        default=ReadingStatus.WANT_TO_READ,
    )

    current_page = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "book"],
                name="unique_user_book",
            )
        ]


class DiaryEntry(models.Model):
    user_book = models.ForeignKey(
        UserBook,
        on_delete=models.CASCADE,
        related_name="diary_entries",
    )

    title = models.CharField(max_length=200)
    content = models.TextField()

    mood = models.CharField(
        max_length=50,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Quote(models.Model):
    user_book = models.ForeignKey(
        UserBook,
        on_delete=models.CASCADE,
        related_name="quoted",
    )

    text = models.TextField()
    page = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
