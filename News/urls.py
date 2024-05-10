from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.NewsList.as_view(), name='news'),
    path('list/<int:pk>', views.NewsArticle.as_view(), name='news'),
    path('users/', views.UsersList.as_view(), name='users'),
    path('users/<int:pk>', views.UserDetail.as_view(), name='user-detail'),
    path('stored/', views.StoredNews.as_view(), name='stored-news'),
    path('stored/<int:pk>', views.StoredNewsDetail.as_view(),
         name='stored-news-detail'),
    path('shared/', views.SharedNewsList.as_view(), name='shared-news'),
    path('shared/<int:destination>',
         views.SharedNewsDetail.as_view(), name='shared-detail'),
    path('bookmarked/<int:user_id>',
         views.BookmarkedNewsList.as_view(), name='bookmarked-news'),
    path('bookmarked/<int:user_id>/<int:news_id>',
         views.BookmarkedNewsDetail.as_view(), name='bookmarked-news-detail'),
    path('follow/<int:follower>', views.FollowList.as_view(), name='follow-list'),
    path('follow/<int:follower>/<int:following>',
         views.FollowDetail.as_view(), name='follow-detail'),
]
