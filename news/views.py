from django.shortcuts import render

from news.models import *


def home(request):
    post = Post.objects.all()
    context = {
        "slider_posts": post.filter(promote=True)[:3],
        "popular_posts": post.order_by('views')[:5],
        "recent_posts": post.order_by('-date')[:5]
    }
    return render(request, "news/home.html", context)
