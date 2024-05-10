from rest_framework.generics import (ListCreateAPIView, RetrieveAPIView,
                                     RetrieveDestroyAPIView,
                                     RetrieveUpdateAPIView)

from . import serializers
from .models import Follow, News, NewsArticle, Share, User


class NewsList(ListCreateAPIView):
    queryset = NewsArticle.objects.all()
    serializer_class = serializers.NewsSerializer


class NewsArticle(RetrieveAPIView):
    queryset = NewsArticle.objects.all()
    serializer_class = serializers.NewsSerializer


class UsersList(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    # Define the fields you want to enable search on
    search_fields = ['username']

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('search', None)
        if search_term:
            queryset = queryset.filter(username__icontains=search_term)
        return queryset


class UserDetail(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class StoredNews(ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = serializers.StoredNewsSerializer


class StoredNewsDetail(RetrieveDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = serializers.StoredNewsSerializer


class SharedNewsList(ListCreateAPIView):
    queryset = Share.objects.all()
    serializer_class = serializers.SharedNewsSerializer


class SharedNewsDetail(ListCreateAPIView):
    serializer_class = serializers.SharedNewsSerializer
    lookup_field = 'destination'

    def get_queryset(self):
        destination = self.kwargs.get('destination')
        source = self.request.query_params.get('source')

        queryset = Share.objects.filter(
            destination=destination)

        if source:
            queryset = queryset.filter(source=source)

        return queryset


class BookmarkedNewsList(ListCreateAPIView):
    serializer_class = serializers.BookmarkedNewsSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return News.objects.filter(bookmarked=True, user_id=user_id)


class BookmarkedNewsDetail(RetrieveDestroyAPIView):
    queryset = News.objects.filter(bookmarked=True).all()
    serializer_class = serializers.BookmarkedNewsSerializer
    lookup_field = 'news_id'


class FollowList(ListCreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = serializers.FollowSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        follower_id = self.kwargs.get('follower')
        following_id = self.request.query_params.get('following')

        if following_id:
            queryset = queryset.filter(
                follower=follower_id, following=following_id)
        elif follower_id:
            queryset = queryset.filter(follower=follower_id)

        return queryset


class FollowDetail(RetrieveDestroyAPIView):
    queryset = Follow.objects.all()
    serializer_class = serializers.FollowSerializer
    lookup_field = 'following'

    def get_queryset(self):
        following_id = self.kwargs['following']
        return Follow.objects.filter(following=following_id)
