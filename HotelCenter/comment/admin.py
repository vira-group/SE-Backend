from django.contrib import admin
from .models import Comment,Tag


admin.site.register(Comment)
admin.site.register(Tag)