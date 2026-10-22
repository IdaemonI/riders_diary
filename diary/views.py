from django.shortcuts import render
from .models import Book


def home(request):
    return render(request, "diary/home.html")


def my_book_list(request):
    books = Book.objects.all()
    context = {
        "books": books,
    }

    return render(request, "diary/book_list.html", context)
