from django.contrib import admin
from .models import Comment,Tag,Reply


admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Reply)