from django.urls import path
from . import api
urlpatterns = [
    path('api/register', api.RegisterApi.as_view()),
]
