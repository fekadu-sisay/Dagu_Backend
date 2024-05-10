from django.contrib.auth.models import AbstractUser
from django.db import models


class Topics(models.Model):
    topic = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name_plural = 'Topics'


class User(AbstractUser):
    topics_selected = models.ManyToManyField(
        Topics, blank=True)
    profile_pic = models.CharField(
        max_length=255, null=True, default="https://res.cloudinary.com/do5keslgr/image/upload/v1711704802/images_rc9qpp.png")


class NewsArticle(models.Model):
    source_name = models.CharField(max_length=100)
    author = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    url = models.URLField()
    url_to_image = models.URLField(blank=True, null=True)
    published_at = models.DateTimeField()
    content = models.TextField()

    def __str__(self):
        return self.title


class News(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE)
    news_id = models.ForeignKey(
        NewsArticle, on_delete=models.CASCADE, null=True, blank=True)
    # url = models.CharField(max_length=500, null=True, blank=True)
    liked = models.BooleanField(default=False)
    bookmarked = models.BooleanField(default=False)

    def __str__(self):
        return self.user_id.username

    class Meta:
        verbose_name_plural = 'News'


class Share(models.Model):
    news_id = models.ForeignKey(
        NewsArticle, on_delete=models.CASCADE)
    source = models.ForeignKey(
        User, related_name='shared_news', on_delete=models.CASCADE)
    destination = models.ForeignKey(
        User, related_name='received_news', on_delete=models.CASCADE)

    def __str__(self):
        return self.source.username


class Follow(models.Model):
    follower = models.ForeignKey(
        User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.follower.username} follows {self.following.username}'
