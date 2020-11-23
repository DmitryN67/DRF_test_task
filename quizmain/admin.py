from django.contrib import admin

from .models import Quiz, Question, Choice, Answer

class QuizAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'description', ]
    date_hierarchy = 'start_date'
    ordering = ['start_date',]

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'question_type', ]

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_text', 'correct', ]

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'question', 'answer_text']


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Answer, AnswerAdmin)
