from django.urls import path, include, re_path

from users.api.views import CurrentUserAPIView


urlpatterns = [
    path('user/', CurrentUserAPIView.as_view(), name='current-user'),
]
