from django.db import models
from django.conf import settings


class Category(models.Model):

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Ticket(models.Model):

    STATUS_CHOICES = [
        ("new", "Новая"),
        ("in_progress", "В работе"),
        ("done", "Выполнена"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Низкий"),
        ("medium", "Средний"),
        ("high", "Высокий"),
    ]

    title = models.CharField(max_length=200)

    description = models.TextField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")

    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default="medium"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="tickets",
        null=True,
        blank=True,
    )

    tags = models.ManyToManyField(
        Tag,
        related_name="tickets",
        blank=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tickets",
    )

    attachment = models.FileField(
        upload_to="tickets/",
        blank=True,
        null=True,
    )


class Comment(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    author = models.CharField(max_length=100)

    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment #{self.pk}"
