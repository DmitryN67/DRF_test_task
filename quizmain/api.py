
from django.contrib.auth.models import User
from django.db.models import F, Count, Value

from rest_framework import generics
from django.contrib.sessions.models import Session

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly ,IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from .permissions import IsAdminOrReadOnly, IsAdminUserOrIsOwner

from .models import Quiz, Question, Choice, Answer, Respondent
from .serializers import QuizSerializer, QuestionSerializer, ChoiceSerializer
from .serializers import AnswerSerializer, UserSerializer, RespondentSerializer
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
        if not self.request.session or not self.request.session.session_key:
            self.request.session.save()
        session = Session.objects.get(pk=self.request.session.session_key)
        quiz = Quiz.objects.get(name=self.request.POST['quiz'])
        if self.request.user.is_authenticated:
            user, created = Respondent.objects.get_or_create(user=self.request.user)
        else:
            user, created = Respondent.objects.get_or_create(session=session)
        user.quiz.add(quiz)    
        serializer.save(user=user)    
        #if not hasattr(self.request, 'answer_text'):
        #    serializer.save(answer_text=serializer.validated_data['hoices'])


class UserViewSet(ModelViewSet):
    
    queryset = Answer.objects.all()
    serializer_class = UserSerializer
    """
    def get_queryset(self):
        #
        #This view should return a list of all the purchases
        #for the currently authenticated user.
        #
        user = self.request.user.id
        return Session.objects.all()
    """

class RespondentViewSet(ReadOnlyModelViewSet):
    
    #queryset = Answer.objects.values('user', 'quiz__name').annotate(count_answers=Count('answer_text'))#annotate(quiz=F('quiz'))
    #queryset = Answer.objects.values('respondent').distinct().annotate(quiz=F('quiz'), answers=F('answer_text'))#annotate(quiz=F('quiz'))
    #queryset = Answer.objects.all()
    queryset = Respondent.objects.all()
    serializer_class = RespondentSerializer

    #permission_classes = [IsAdminOrReadOnly]
    
   