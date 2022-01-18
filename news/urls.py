from django.urls import path
from news import views

urlpatterns = [
    path('', views.home_view, name="home"),
    path('news-list/', views.news_list_view, name="news-list"),
    path('search_result/', views.search_result_view, name="search"),
    path('news-details/<int:post_id>/', views.news_details_view),
    path('add-news/', views.add_news_view, name="add-news"),
    path('edit-news/<int:post_id>/', views.edit_news),
    path('delete-news/<int:post_id>/', views.delete_news),
    path('comment-validation/<int:comment_id>/', views.comment_validation_view),
    path('delete-comment/<int:comment_id>/', views.delete_comment_view)
]
