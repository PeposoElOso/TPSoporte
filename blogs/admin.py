from django.contrib import admin
from blogs.models import Post, Category, Comment, Album,Artist
# Register your models here.


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Album)
admin.site.register(Artist)