from django.db.models import Count, Q
from django.shortcuts import render

from news.models import *
from news.utils import *
from news.forms import *


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
    filter_form = FilterForm()
    main_posts = posts

    if request.GET.get("start_date") and request.GET.get("end_date"):
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        main_posts = posts.filter(date__gte=start_date, date__lt=end_date)
    if request.GET.get("choice_field") == "بازدید - (زیاد به کم)":
        main_posts = main_posts.order_by("-views")
    elif request.GET.get("choice_field") == "بازدید - (کم به زیاد)":
        main_posts = main_posts.order_by("views")
    elif request.GET.get("choice_field") == "تاریخ - (جدید به قدیم)":
        main_posts = main_posts.order_by("-date")
    elif request.GET.get("choice_field") == "تاریخ - (قدیم به جدید)":
        main_posts = main_posts.order_by("date")

    context = {
        "popular_posts_view": pagination(posts.order_by('views'), 3, popular_view_page_num),
        "popular_posts_comments": pagination(posts.annotate(num=Count("comments")).order_by("-num"), 3,
                                             popular_comments_page_num),
        "main_posts": pagination(main_posts, 3, main_page_num),
        "filter_form": filter_form
    }
    return render(request, "news/news-list.html", context)


def search_result(request):
    main_page_num = request.GET.get('main_page_num')

    search = request.GET.get("search")
    print(main_page_num)
    main_posts = Post.objects.all().filter(Q(title__icontains=search) | Q(text__icontains=search))
    context = {
        "main_posts": pagination(main_posts, 1, main_page_num),
        "search": search,
    }
    return render(request, "news/search-result.html", context)


def news_details(request, post_id):
    post = Post.objects.get(pk=post_id)
    context = {
        "post": post,
        "popular_posts": Post.objects.all().order_by('views')[:5],
        "recent_posts": Post.objects.all().order_by('-date')[:5],
    }
    return render(request, "news/news-details.html", context)
