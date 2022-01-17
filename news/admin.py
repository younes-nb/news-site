from django.contrib import admin
from news.models import Post
from news.models import Comment

admin.site.register(Post)
admin.site.register(Comment)
