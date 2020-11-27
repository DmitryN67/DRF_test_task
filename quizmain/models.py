from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


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

    question = models.ForeignKey(Question, verbose_name="Вопрос", on_delete=models.CASCADE, related_name='choice')
    choice_text = models.CharField(verbose_name="Вариант ответа",max_length=300)
    correct = models.BooleanField(verbose_name="Правильный вариант",default=False)

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответа"

    def __str__(self):
        return self.choice_text


class Answer(models.Model):
    """Класс ответов на вопросы"""

    #user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, related_name='user_answer', blank=True, null=True)
    user = models.PositiveIntegerField()
    question = models.ForeignKey(Question, verbose_name="Вопрос", on_delete=models.DO_NOTHING, related_name='question_answer')
    choices = models.ForeignKey(Choice, verbose_name="Варианты", on_delete=models.DO_NOTHING, related_name='choice_answer', blank=True, null=True)
    answer_text = models.CharField(verbose_name="Ответ", max_length=50)

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return self.answer_text
