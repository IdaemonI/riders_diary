from django.contrib import admin

from .models import Ticket, Category, Tag, Comment

admin.site.register(Ticket)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
