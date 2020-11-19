from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer, RelatedField

from .models import Quiz, Question, Answer


class AnswerListSerializer(ModelSerializer):
    """Список ответов"""

    class Meta:
        model = Answer
        fields = ('answer_text',)


class QuizListSerializer(ModelSerializer):
    """Список опросов"""
    
    class Meta:
        model = Quiz
        fields = ('__all__')


class QuestionListSerializer(ModelSerializer):
    """Список вопросов"""
    answers = AnswerListSerializer(many=True)
    class Meta:
        model = Question
        fields = ('question_text', 'answers')


class QuizDetailSerializer(ModelSerializer):
    #questions = RelatedField(source='quiz', read_only=True)
    questions = QuestionListSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ('name', 'date_start', 'date_end', 'description', 'questions')