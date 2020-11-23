from rest_framework.routers import SimpleRouter
from .api import QuizPassView, ActiveQuizView
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
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns += router.urls
