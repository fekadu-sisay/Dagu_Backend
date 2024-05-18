from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import (ListCreateAPIView, RetrieveAPIView,
                                     RetrieveDestroyAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.response import Response

from . import serializers
from .models import Follow, News, NewsArticle, Share, User


@api_view(['GET', 'POST'])
def create_news_article(request):
    if request.method == 'POST':
        serializer = serializers.NewsSerializer(data=request.data)
        if serializer.is_valid():
            news_article = serializer.save()
            response_data = {
                'success': True,
                'message': 'News article created successfully.',
                'news_id': news_article.id
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({'success': False, 'message': 'Invalid data provided.'}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        news_articles = NewsArticle.objects.all()
        serializer = serializers.NewsSerializer(
            news_articles, many=True)
        return Response(serializer.data)


class NewsArticles(RetrieveAPIView):
    queryset = NewsArticle.objects.all()
    serializer_class = serializers.NewsSerializer


class UsersList(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
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

class StoredNewsDetail(ListAPIView):
    serializer_class = serializers.StoredNewsSerializer
    lookup_field = 'news_id'

    def get_queryset(self):
        news_id = self.kwargs.get(self.lookup_field)
        return News.objects.filter(news_id=news_id, liked=True)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)


class SharedNewsList(ListCreateAPIView):
    queryset = Share.objects.all()
    serializer_class = serializers.SharedNewsSerializer


class SharedNewsDetail(ListCreateAPIView):
    serializer_class = serializers.SharedNewsDetailSerializer
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


class LikedNewsList(ListCreateAPIView):
    serializer_class = serializers.LikedNewsSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return News.objects.filter(liked=True, user_id=user_id)


class LikedNewsDetail(RetrieveDestroyAPIView):
    queryset = News.objects.filter(liked=True).all()
    serializer_class = serializers.LikedNewsSerializer
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
