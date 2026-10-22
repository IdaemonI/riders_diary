from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("tickets/", views.ticket_list, name="ticket_list"),
    path("about/", views.about, name="about"),
    path("stats/", views.stats, name="stats"),
    path("tickets/create/", views.ticket_create, name="ticket_create"),
    path("tickets/<int:pk>/", views.ticket_detail, name="ticket_detail"),
    path("tickets/<int:pk>/edit", views.ticket_edit, name="ticket_edit"),
    path("tickets/<int:pk>/delete", views.ticket_delete, name="ticket_delete"),
    path("tickets/<int:pk>/close", views.ticket_close, name="ticket_close"),
    path("tickets/<int:pk>/to_work", views.ticket_to_work, name="ticket_to_work"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/<int:pk>/", views.category_tickets, name="category_tickets"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
