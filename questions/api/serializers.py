from rest_framework import serializers
from questions.models import Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    created_at = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    user_has_voted = serializers.SerializerMethodField()
    question_slug = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        exclude = ['question', 'voters', 'updated_at']

    @staticmethod
    def get_created_at(instance):
        return instance.created_at.strftime("%d %B %Y")

    @staticmethod
    def get_likes_count(instance):
        return instance.voters.count()

    def get_user_has_voted(self, instance):
        request = self.context.get('request')
        return instance.voters.filter(pk=request.user.pk).exists()

    @staticmethod
    def get_question_slug(instance):
        return instance.question.slug


class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    created_at = serializers.SerializerMethodField()
    slug = serializers.SlugField(read_only=True)
    answers_count = serializers.SerializerMethodField()
    user_has_answered = serializers.SerializerMethodField()

    class Meta:
        model = Question
        exclude = ["updated_at"]

    @staticmethod
    def get_created_at(instance):
        return instance.created_at.strftime("%d %B %Y")

    @staticmethod
    def get_answers_count(instance):
        return instance.answers.count()

    def get_user_has_answered(self, instance):
        request = self.context.get('request')
        return instance.answers.filter(author=request.user.pk).exists()





