from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session


class Quiz(models.Model):
    """Класс опроса"""

    name = models.CharField(verbose_name="Название опроса", max_length=50)
    start_date = models.DateField(verbose_name="Дата начала", auto_now=False, auto_now_add=False)
    end_date = models.DateField(verbose_name="Дата окончания", auto_now=False, auto_now_add=False)
    description = models.TextField(verbose_name="Описание")


    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"

    def __str__(self):
        return self.name


class Question(models.Model):
    """Класс вопроса"""
    
    QUESTION_TYPES = (
        ('text', 'Ответ с текстом'),
        ('choose_one', 'Выбор одного варианта'),
        ('choose_many', 'Выбор нескольких вариантов'),
    )

    quiz = models.ForeignKey(Quiz, verbose_name="Опрос",  on_delete=models.CASCADE, related_name='question')
    question_text = models.TextField(verbose_name="Вопрос")
    question_type = models.CharField(verbose_name="Тип вопроса", max_length=50, choices=QUESTION_TYPES)


    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    """Класс вариантов ответов на вопросы с возможностью выбора"""

    question = models.ForeignKey(Question, verbose_name="Вопрос", on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(verbose_name="Вариант ответа",max_length=300)
    correct = models.BooleanField(verbose_name="Правильный вариант",default=False, blank=True, null=True)

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответа"

    def __str__(self):
        return self.choice_text


class Respondent(models.Model):
    """Класс респондентов"""
    
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, blank=True, null=True)
    session = models.CharField(verbose_name="Сессия", max_length=100)
    quiz = models.ManyToManyField(Quiz, verbose_name="Опрос", related_name='quiz_respondent')

    def __str__(self):
        if self.user is None:
            return 'Anonymous'
        return self.user.username


class Answer(models.Model):
    """Класс ответов на вопросы"""

    user = models.ForeignKey(Respondent, verbose_name="Пользователь", on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, verbose_name="Опрос", on_delete=models.CASCADE, related_name='quiz_answer')
    question = models.ForeignKey(Question, verbose_name="Вопрос", on_delete=models.CASCADE, related_name='question_answer')
    choices = models.ManyToManyField(Choice, verbose_name="Варианты", related_name='choice_answer', blank=True)
    answer_text = models.CharField(verbose_name="Ответ", max_length=50, blank=True)

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        if self.answer_text == '':
            return ', '.join([choice for choice in self.choices.all().values_list('choice_text', flat=True)])
        return self.answer_text
