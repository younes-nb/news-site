from django.shortcuts import render

from news.models import *


def home(request):
    post = Post.objects.all()
    context = {
        "slider_post": post.filter(promote=True)
    }
    return render(request, "news/home.html", context)
