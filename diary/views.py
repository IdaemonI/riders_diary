from django.shortcuts import render
from models import Book


def home(request):
    return render(request, "diary/home.html")


def book_list(request):
    Book.models.ge
