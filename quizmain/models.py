from django.db import models


class Quiz(models.Model):
    """Класс опроса"""

    name = models.CharField(verbose_name="Название опроса", max_length=50)
    start_date = models.DateField(verbose_name="Дата старта", auto_now=False, auto_now_add=False)
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
        ('T', 'Ответ с текстом'),
        ('CO', 'Выбор одного варианта'),
        ('CM', 'Выбор нескольких вариантов'),
    )

    quiz = models.ForeignKey(Quiz, verbose_name="Опрос",  on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField(verbose_name="Текст вопроса")
    question_type = models.CharField(verbose_name="Тип вопроса", max_length=50, choices=QUESTION_TYPES)


    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    """Класс вариантов ответов на вопросы с возможностью выбора"""

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=300)
    correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответа"

    def __str__(self):
        return self.choice_text


class Answer(models.Model):
    """Класс ответов на вопросы"""

    user_id = models.PositiveIntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question')
    choice = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choice')
    answer_text = models.CharField(max_length=300)

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return self.answer_text
