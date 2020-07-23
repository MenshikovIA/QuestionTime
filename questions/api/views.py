from rest_framework import viewsets, generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from questions.api.permissions import IsAuthorOrReadOnly
from questions.api.serializers import QuestionSerializer, AnswerSerializer
from questions.models import Question, Answer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('-created_at')
    lookup_field = "slug"
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AnswerCreateApiView(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request_user = self.request.user
        kwarg_slug = self.kwargs.get("slug")
        question = get_object_or_404(Question, slug=kwarg_slug)

        if question.answers.filter(author=request_user).exists():
            raise ValidationError("You have already answered that question!")

        serializer.save(author=request_user, question=question)


class AnswersListApiView(generics.ListAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return Answer.objects.filter(question__slug=slug).order_by("-created_at")


class AnswerRUDApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]


class LikeApiView(APIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        user = request.user

        answer.voters.add(user)
        answer.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        user = request.user

        answer.voters.remove(user)
        answer.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)
