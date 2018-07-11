from django.urls import path, reverse
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('index', views.NewsList.as_view(), name='index'),
    path('index/<int:pk>', views.NewsTagDetail.as_view(), name='tag-detail'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('account', views.account, name='account'),
    path('account/logout', views.logout, name='account-logout'),
    path('details/<int:pk>', views.NewsDetail.as_view(), name='news-details'),
    path('favorite/<int:pk>', views.favroite_news, name="news-favorited"),
    path('favorite/<int:pk>/<int:f>', views.favorite_news_post, name="news-favorited-post"),
    path('comment/<int:pk>/<str:content>', views.comment_post, name="comment-post"),
    path('search/<str:content>', views.search, name="search"),
    path('account/news/publish', views.publish_news, name="news-publish"),
]