from rest_framework.routers import SimpleRouter
from .api import ActiveQuizView, RespondentViewSet
from .api import QuizViewSet, QuestionViewSet, ChoiceViewSet, AnswerViewSet
from django.urls import path, include
from .models import Quiz


router = SimpleRouter()

router.register('quiz/active', ActiveQuizView)
router.register('quiz', QuizViewSet)
router.register('question', QuestionViewSet)
router.register('choice', ChoiceViewSet)
router.register('answer', AnswerViewSet)
router.register('respondent', RespondentViewSet)


urlpatterns = [
    path('api-auth/', include('rest_framework.urls'))
]

urlpatterns += router.urls
