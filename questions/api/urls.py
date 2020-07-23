from django.urls import include, path
from rest_framework.routers import DefaultRouter

from questions.api import views as qv


router = DefaultRouter()
router.register(r"questions", qv.QuestionViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("questions/<slug:slug>/answers/", qv.AnswersListApiView.as_view(), name='answers-list'),
    path("questions/<slug:slug>/answer/", qv.AnswerCreateApiView.as_view(), name='answer-create'),
    path("answers/<int:pk>/", qv.AnswerRUDApiView.as_view(), name='answer-detail'),
    path("answers/<int:pk>/like/", qv.LikeApiView.as_view(), name='answer-like'),
]