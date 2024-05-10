from rest_framework import serializers

from .models import Follow, News, NewsArticle, Share, Topics, User


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsArticle
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = ('id', 'topic')


class UserSerializer(serializers.ModelSerializer):
    topics_selected = TopicSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',
                  'email', 'topics_selected', 'profile_pic', 'last_login')

    def update(self, instance, validated_data):
        topics_data = validated_data.pop('topics_selected')
        instance = super().update(instance, validated_data)
        for topic_data in topics_data:
            topic, _ = Topics.objects.get_or_create(**topic_data)
            instance.topics_selected.add(topic)
        return instance


class StoredNewsSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(
        source='user_id.first_name', read_only=True)
    news_topic = serializers.CharField(source='news_id.title', read_only=True)

    class Meta:
        model = News
        fields = ('id', 'liked', 'bookmarked', 'user_id',
                  'user_name', 'news_id', 'news_topic')


class SharedNewsSerializer(serializers.ModelSerializer):
    news_id = NewsSerializer()
    source_name = serializers.CharField(
        source='source.first_name', read_only=True)
    source_profile = serializers.URLField(
        source='source.profile_pic', read_only=True)

    class Meta:
        model = Share
        fields = ('id', 'news_id', 'source', 'source_profile',
                  'source_name', 'destination')


class BookmarkedNewsSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(
        source="user_id.username", read_only=True)
    news = NewsSerializer(source="news_id", read_only=True)

    class Meta:
        model = News
        fields = ('user_id', 'user_name', 'news_id', 'news', 'bookmarked')


class FollowSerializer(serializers.ModelSerializer):
    followed_user = UserSerializer(source="following", read_only=True)

    class Meta:
        model = Follow
        fields = ('follower', 'following', 'followed_user')
