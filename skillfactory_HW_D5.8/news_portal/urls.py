import os
from django.urls import path
# Импортируем созданное нами представление
from .views import NewsListView, NewsDetailView, ArticleDetailView,NewsSearchView, NewsCreateView, NewsUpdateView, NewsDeleteView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView




urlpatterns = [
    path('', NewsListView.as_view(), name='news_list'),
    path('news/<int:pk>', NewsDetailView.as_view(), name='news_detail'),
    path('articles/<int:pk>', ArticleDetailView.as_view(), name='article_detail'),
    path('search/', NewsSearchView.as_view(), name='news_search'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),

    # остальные URL-шаблоны вашего проекта
]