
from django.contrib.auth.models import User

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly ,IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from .permissions import IsAdminOrReadOnly, IsAdminUserOrIsOwner

from .models import Quiz, Question, Choice, Answer
from .serializers import QuizSerializer, QuestionSerializer, ChoiceSerializer
from .serializers import AnswerSerializer, UserSerializer
from .util import token_to_int

from datetime import datetime


class ActiveQuizView(ModelViewSet):
    queryset = Quiz.objects.filter(start_date__lte=datetime.today(), end_date__gte=datetime.today())
    serializer_class = QuizSerializer
    permission_classes = [IsAdminOrReadOnly]


class QuizViewSet(ModelViewSet):

    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAdminOrReadOnly]    


class QuestionViewSet(ModelViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ChoiceViewSet(ModelViewSet):

    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [IsAdminOrReadOnly]


class AnswerViewSet(ModelViewSet):

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user.id)
        else:
            serializer.save(user=token_to_int(self.request.COOKIES['csrftoken'], 8))


class UserAnswerViewSet(ModelViewSet):
    
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]
   