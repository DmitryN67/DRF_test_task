
from rest_framework import mixins
from rest_framework import generics

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response

from .permissions import IsAdminOrReadOnly, IsAdminOrIsOwner

from .models import Quiz, Question, Choice, Answer
from .serializers import QuizSerializer, QuizDetailSerializer, QuestionSerializer, ChoiceSerializer, AnswerSerializer, QuizPassSerializer

from datetime import datetime


class ActiveQuizView(ModelViewSet):
    queryset = Quiz.objects.filter(start_date__lte=datetime.today(), end_date__gte=datetime.today())
    serializer_class = QuizSerializer
    permission_classes = [IsAdminOrReadOnly]


class QuizPassView(ModelViewSet):
    queryset = Quiz.objects.filter(start_date__lte=datetime.today(), end_date__gte=datetime.today())
    serializer_class = QuizPassSerializer


class QuizViewSet(ModelViewSet):

    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAdminOrReadOnly]    


class QuestionViewSet(ModelViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAdminOrReadOnly]        


class ChoiceViewSet(ModelViewSet):

    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [IsAdminOrReadOnly]


class AnswerViewSet(ModelViewSet):

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAdminOrIsOwner]