from django.contrib import admin
from .models import News, Share, Topics, User, Follow, NewsArticle

admin.site.register(User)
admin.site.register(News)
admin.site.register(Share)
admin.site.register(Topics)
admin.site.register(Follow)
admin.site.register(NewsArticle)
