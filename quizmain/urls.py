from rest_framework.routers import SimpleRouter
from .api import QuizListView, QuizDetailView, QuizPassView, ActiveQuizView
from .api import QuestionListView, QuestionDetailView
from .api import ChoiceListView, ChoiceDetailView
from .api import AnswerListView, AnswerDetailView
from .api import QuizViewSet, QuestionViewSet, ChoiceViewSet, AnswerViewSet
from django.urls import path, include
from .models import Quiz



quiz_list = QuizViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
quiz_detail = QuizViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


router = SimpleRouter()


router.register('quiz/active', ActiveQuizView)
router.register('quiz/pass', QuizPassView)
router.register('quiz', QuizViewSet)
router.register('question', QuestionViewSet)
router.register('choice', ChoiceViewSet)
router.register('answer', AnswerViewSet)



urlpatterns = [
    path('api-auth/login/', include('rest_framework.urls')),
    #path('quiz/create/', QuizListView.as_view()),
    #path('quiz/update/<int:pk>/', QuizDetailView.as_view()),
    #path('quiz/view/', QuizListView.as_view()),
    #path('question/create/', QuestionListView.as_view()),
    #path('question/update/<int:pk>/', QuestionDetailView.as_view()),
    #path('choice/create/', ChoiceListView.as_view()),
    #path('choice/update/<int:pk>/',ChoiceDetailView.as_view()),
    #path('answer/create/', AnswerListView.as_view()),
    #path('answer/view/<int:pk>/', AnswerListView.as_view()),
    #path('answer/update/<int:pk>/', AnswerDetailView.as_view()),
]

urlpatterns += router.urls
