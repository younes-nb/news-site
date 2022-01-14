from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from news.models import *


def home(request):
    post = Post.objects.all()
    paginator = Paginator(post, 10)
    page = request.GET.get('page', 1)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        "slider_posts": post.filter(promote=True)[:3],
        "popular_posts": post.order_by('views')[:5],
        "recent_posts": post.order_by('-date')[:5],
        "main_posts": posts
    }
    return render(request, "news/home.html", context)
