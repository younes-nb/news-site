from django.urls import path
from news.views import *

urlpatterns = [
    path('', home, name="home"),
    path('news-list/', news_list, name="news-list"),
    path('search_result/', search_result,name="search"),
    path('news-details/<int:post_id>/', news_details)
]
