from django.test import TestCase
from quizmain.models import Quiz
from quizmain.serializers import QuizSerializer
from datetime import date

#class QuizSerializerTestCase(TestCase):
    #def test_quiz_serializer(self):
        #quiz_1 = Quiz.objects.create(name='Quiz_1', start_date="2020-12-01", end_date="2020-12-15", description='Quiz_1 description')
        #quiz_2 = Quiz.objects.create(name='Quiz_2', start_date='2020-12-02', end_date='2020-12-16', description='Quiz_2 description')
        #data = QuizSerializer([quiz_1, quiz_2], many=True).data
        #print(data)
        #expected_data = [
            #{
                #'name': 'Quiz_1',
                #'start_date': "2020-12-01",
                #'end_date': "2012-12-15",
                #'description': 'Quiz_1 description',
                #'question': ''
            #},
            #{
                #'name': 'Quiz_2',
                #'start_date': '2020-12-02',
                #'end_date': '2012-12-16',
                #'description': 'Quiz_2 description',
                #'question': ''
            #},
        #]
        #self.assertEqual(expected_data, data)

 #class ChoiceSerializerTestCase(TestCase):
     #def test_choice_serializer(self):
         #choice_1 = Choice.objects.create()