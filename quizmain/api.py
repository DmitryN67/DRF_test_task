
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Quiz, Question
from .serializers import QuizListSerializer, QuestionListSerializer, QuizDetailSerializer


from datetime import datetime

class QuizListView(ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizListSerializer


class ActualQuizView(ModelViewSet):
    queryset = Quiz.objects.filter(date_end__gte=datetime.today())
    serializer_class = QuizListSerializer


class QuizDetailView(ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizDetailSerializer
    

class QuestionListView(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionListSerializer    