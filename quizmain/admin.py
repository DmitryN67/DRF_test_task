from django.contrib import admin

from .models import Quiz, Question, Answer

class QuizAdmin(admin.ModelAdmin):
    list_display = ['name', 'date_start', 'date_end', 'description', ]
    date_hierarchy = 'date_start'
    ordering = ['date_start',]

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'question_type', ]

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['answer_text', 'correct', ]
    

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)