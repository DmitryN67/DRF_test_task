from rest_framework.routers import SimpleRouter
from .api import QuizListView, QuestionListView, ActualQuizView, QuizDetailView
from django.urls import path, include
from .views import MyLoginView

router = SimpleRouter()

router.register('api/quizes', QuizListView)
router.register('api/questions', QuestionListView)
router.register('api/actualquizes', ActualQuizView)
router.register('api/quiz', QuizDetailView)

urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
]


urlpatterns += router.urls