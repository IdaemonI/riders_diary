from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("mybooks/", views.my_book_list, name="my_book_list"),
]
