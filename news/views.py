from django.db.models import Count
from django.shortcuts import render

from news.models import *
from news.utils import *


def home(request):
    posts = Post.objects.all()
    main_page_num = request.GET.get('main_page_num', 1)
    context = {
        "slider_posts": posts.filter(promote=True)[:3],
        "popular_posts": posts.order_by('views')[:5],
        "recent_posts": posts.order_by('-date')[:5],
        "main_posts": pagination(posts, 10, main_page_num)
    }
    return render(request, "news/home.html", context)


def news_list(request):
    posts = Post.objects.all()
    main_page_num = request.GET.get('main_page_num', 1)
    popular_comments_page_num = request.GET.get('popular_comments_page_num', 1)
    popular_view_page_num = request.GET.get('popular_view_page_num', 1)
    context = {
        "popular_posts_view": pagination(posts.order_by('views'), 3, popular_view_page_num),
        "popular_posts_comments": pagination(posts.annotate(num=Count("comments")).order_by("-num"), 3,
                                             popular_comments_page_num),
        "main_posts": pagination(posts, 10, main_page_num)
    }
    return render(request, "news/news-list.html", context)
