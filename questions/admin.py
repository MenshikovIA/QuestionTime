from django.contrib import admin
from questions.models import Question, Answer


class QuestionAdmin(admin.ModelAdmin):
    exclude = ('slug',)


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
