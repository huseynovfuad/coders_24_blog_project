from django.contrib import admin
from .models import Blog, BlogImage, Comment

# Register your models here.


class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    list_display_links = ("id", "title")

admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogImage)
admin.site.register(Comment)