from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def pagination(posts, pages, page_num):
    paginator = Paginator(posts, pages)
    try:
        result = paginator.page(page_num)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)

    return result
