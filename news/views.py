from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from News_Site import settings
from news.forms import FilterForm, NewsForm, CommentForm, CommentValidationForm
from news.models import Post, Comment
from news.utils import pagination


def home_view(request):
    posts = Post.objects.all()
    main_page_num = request.GET.get('main_page_num', 1)
    context = {
        "slider_posts": posts.filter(promote=True)[:3],
        "popular_posts": posts.order_by('views')[:5],
        "recent_posts": posts.order_by('-date')[:5],
        "main_posts": pagination(posts, 10, main_page_num)
    }
    return render(request, "news/home.html", context)


def news_list_view(request):
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


def search_result_view(request):
    main_page_num = request.GET.get('main_page_num')

    search = request.GET.get("search")
    print(main_page_num)
    main_posts = Post.objects.all().filter(Q(title__icontains=search) | Q(text__icontains=search))
    context = {
        "main_posts": pagination(main_posts, 1, main_page_num),
        "search": search,
    }
    return render(request, "news/search-result.html", context)


def news_details_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.views += 1
    post.save()

    comments = post.comments.filter(is_valid=True, parent__isnull=True)
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            parent = None
            try:
                parent_id = int(request.POST.get("parent_id"))
            except:
                parent_id = None
            if parent_id:
                parent = Comment.objects.get(id=parent_id)
                if parent:
                    reply_comment = comment_form.save(commit=False)
                    reply_comment.parent = parent
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect("/news-details/{}/".format(post.id))
    else:
        comment_form = CommentForm()
    context = {
        "post": post,
        "comments": comments,
        "comment_form": comment_form,
        "popular_posts": Post.objects.all().order_by('views')[:5],
        "recent_posts": Post.objects.all().order_by('-date')[:5],
    }
    return render(request, "news/news-details.html", context)


# @login_required
# def comment_validation_view(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)
#     if request.user == post.author:
#         if request.method == "POST":
#             comment_form = CommentValidationForm(request.POST)


@login_required
def add_news_view(request):
    if request.method == "POST":
        news_form = NewsForm(request.POST, request.FILES)
        if news_form.is_valid():
            post = Post(author=request.user, title=news_form.cleaned_data["title"], text=news_form.cleaned_data["text"],
                        image=news_form.cleaned_data["image"],
                        promote=news_form.cleaned_data["promote"])
            post.save()
            return redirect("/news-details/{}/".format(post.id))
    else:
        news_form = NewsForm()
    context = {
        "form": news_form,
    }
    return render(request, "news/add-news.html", context)


@login_required
def edit_news(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user == post.author:
        if request.method == "POST":
            news_form = NewsForm(request.POST, request.FILES, instance=post)
            if news_form.is_valid():
                news_form.save()
                return redirect("/news-details/{}/".format(post.id))
        else:
            news_form = NewsForm(instance=post)
        context = {
            "form": news_form,
        }
        return render(request, "news/edit-news.html", context)
    return HttpResponseForbidden(request)


@login_required
def delete_news(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user == post.author:
        post.delete()
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
    return HttpResponseForbidden(request)
