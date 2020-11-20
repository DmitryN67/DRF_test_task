from rest_framework.serializers import ModelSerializer, RelatedField
from rest_framework.serializers import ValidationError
from rest_framework.serializers import ReadOnlyField

from .models import Quiz, Question, Choice, Answer


class ChoiceSerializer(ModelSerializer):
    """Список вариантов ответов на вопросы с возможностью выбора"""

    class Meta:
        model = Choice
        fields = ['question', 'choice_text', 'correct', ]   


class QuizSerializer(ModelSerializer):
    """Список опросов"""

    class Meta:
        model = Quiz
        fields = ['name', 'start_date', 'end_date', 'description']


class QuestionSerializer(ModelSerializer):
    """Список вопросов"""
    choices = ChoiceSerializer(many=True)
    class Meta:
        model = Question
        fields = ('question_text', 'choices')


class QuizDetailSerializer(ModelSerializer):
    #questions = RelatedField(source='quiz', read_only=True)
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ('name', 'start_date', 'end_date', 'description', 'questions')


class AnswerSerializer(ModelSerializer):
    """Список вопросов"""
    question = QuestionSerializer()
    choice = ChoiceSerializer(many=True)
    class Meta:
        model = Answer
        fields = ('user_id', 'question', 'choice', 'answer_text')


class QuizPassSerializer(ModelSerializer):
    """Прохождение опроса"""
    questions = QuestionSerializer(many=True)


    class Meta:
        model = Quiz
        fields = ('name', 'description', 'questions')
