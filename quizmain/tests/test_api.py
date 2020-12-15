from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from quizmain.models import Quiz, Question, Choice, Answer
from quizmain.serializers import QuizSerializer, QuestionSerializer, ChoiceSerializer, AnswerSerializer
from django.contrib.auth.models import User
from json import dumps

class QuizAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='admin', password='admin', is_superuser=True, is_staff=True)
        self.client.force_login(self.user)
        self.quiz_1 = Quiz.objects.create(name='Quiz_1', start_date='2020-12-01', end_date='2020-12-15', description='Quiz_1 description')
        self.quiz_2 = Quiz.objects.create(name='Quiz_2', start_date='2020-12-02', end_date='2020-12-16', description='Quiz_2 description')
        self.quiz_3 = Quiz.objects.create(name='Quiz_3', start_date='2020-12-03', end_date='2020-12-17', description='Quiz_3 description')
        self.create_valid_data = {
            'name': 'Quiz_4',
            'start_date': '2020-12-04',
            'end_date': '2020-12-18',
            'description': 'Quiz_4 description'
        }
        self.create_invalid_data = {
            'name': 'Quiz_5',
            'start_date': '',
            'end_date': '2020-12-18',
            'description': 'Quiz_4 description'
        }
        self.update_valid_data = {
            'name': self.quiz_1.name,
            'start_date': self.quiz_1.start_date,
            'end_date': self.quiz_1.end_date,
            'description': 'Quiz_1 new description'
        }
        self.update_invalid_data = {
            'name': '',
            'start_date': self.quiz_1.start_date,
            'end_date': self.quiz_1.end_date,
            'description': 'Quiz_1 new description'
        }


    def test_quiz_valid_create(self):
        self.assertEqual(3, Quiz.objects.all().count())
        url = reverse('quiz-list')
        json_data = dumps(self.create_valid_data)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Quiz.objects.all().count())

    def test_quiz_invalid_create(self):
        url = reverse('quiz-list')
        json_data = dumps(self.create_invalid_data)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(3, Quiz.objects.all().count())

    def test_quiz_read_valid_single(self):
        url = reverse('quiz-detail', args=(self.quiz_1.id,))
        response = self.client.get(url)
        serializer_data = QuizSerializer(self.quiz_1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_quiz_read_invalid_single(self):
        url = reverse('quiz-detail', args=(100500,))
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
    
    def test_quiz_list_read(self):
        url = reverse('quiz-list')
        response = self.client.get(url)
        serializer_data = QuizSerializer([self.quiz_1, self.quiz_2, self.quiz_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_quiz_valid_update(self):
        url = reverse('quiz-detail', args=(self.quiz_1.id,))

        json_data = dumps(self.update_valid_data)
        response = self.client.put(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.quiz_1.refresh_from_db()
        self.assertEqual('Quiz_1 new description', self.quiz_1.description)

    def test_quiz_invalid_update(self):
        url = reverse('quiz-detail', args=(self.quiz_1.id,))

        json_data = dumps(self.update_invalid_data)
        response = self.client.put(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_quiz_valid_delete(self):
        self.assertEqual(3, Quiz.objects.all().count())
        url = reverse('quiz-detail', args=(self.quiz_3.id,))
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Quiz.objects.all().count())

    def test_quiz_invalid_delete(self):
        self.assertEqual(3, Quiz.objects.all().count())
        url = reverse('quiz-detail', args=(100500,))
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(3, Quiz.objects.all().count())


class QuiestionAPItestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='admin', password='admin', is_superuser=True, is_staff=True)
        self.client.force_login(self.user)
        self.quiz_1 = Quiz.objects.create(name='Quiz_1', start_date='2020-12-01', end_date='2020-12-15', description='Quiz_1 description')
        self.quiz_2 = Quiz.objects.create(name='Quiz_2', start_date='2020-12-02', end_date='2020-12-16', description='Quiz_2 description')
        self.question_1 = Question.objects.create(quiz=self.quiz_1, question_text='Question with text answer', question_type='text')
        self.question_2 = Question.objects.create(quiz=self.quiz_1, question_text='Question with choose one', question_type='choose one')
        self.question_3 = Question.objects.create(quiz=self.quiz_1, question_text='Question with choose many', question_type='choose many')

        self.create_valid_data = {
            'quiz': self.quiz_2.name,
            'question_text': 'Question for quiz_2',
            'question_type': 'choose_one',
        }
        self.create_invalid_data = {
            'quiz': '',
            'question_text': 'Question for quiz_2',
            'question_type': 'choose_one',
        }
        self.update_valid_data = {
            'quiz': self.question_1.quiz.name,
            'question_text': 'Updated question with text answer',
            'question_type': self.question_1.question_type,
        }
        self.update_invalid_data = {
            'quiz': self.question_1.quiz.id,
            'question_text': 'Updated question with text answer',
            'question_type': '',
        }


    def test_question_valid_create(self):
        self.assertEqual(3, Question.objects.all().count())
        url = reverse('question-list')
        json_data = dumps(self.create_valid_data)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Question.objects.all().count())

    def test_question_invalid_create(self):
        url = reverse('question-list')
        json_data = dumps(self.create_invalid_data)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(3, Question.objects.all().count())

    def test_question_read_valid_single(self):
        url = reverse('question-detail', args=(self.quiz_1.id,))
        response = self.client.get(url)
        serializer_data = QuestionSerializer(self.question_1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_question_read_invalid_single(self):
        url = reverse('question-detail', args=(100500,))
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
    
    def test_question_list_read(self):
        url = reverse('question-list')
        response = self.client.get(url)
        serializer_data = QuestionSerializer([self.question_1, self.question_2, self.question_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_question_valid_update(self):
        url = reverse('question-detail', args=(self.question_1.id,))

        json_data = dumps(self.update_valid_data)
        response = self.client.put(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.question_1.refresh_from_db()
        self.assertEqual('Updated question with text answer', self.question_1.question_text)

    def test_question_invalid_update(self):
        url = reverse('question-detail', args=(self.question_1.id,))

        json_data = dumps(self.update_invalid_data)
        response = self.client.put(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_question_valid_delete(self):
        self.assertEqual(3, Question.objects.all().count())
        url = reverse('question-detail', args=(self.question_3.id,))
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Question.objects.all().count())

    def test_question_invalid_delete(self):
        self.assertEqual(3, Question.objects.all().count())
        url = reverse('question-detail', args=(100500,))
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(3, Question.objects.all().count())


class ChoiceAPItestCase(APITestCase):

    def test_choice_get(self):
        pass

    def test_choice_post(self):
        pass

    def test_choice_put(self):
        pass

    def test_choice_delete(self):
        pass


class AnswerAPItestCase(APITestCase):

    def test_answer_get(self):
        pass

    def test_answer_post(self):
        pass

    def test_answer_put(self):
        pass

    def test_answer_delete(self):
        pass    






        