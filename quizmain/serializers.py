from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ValidationError

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db.models import F, Count, Value

from .util import token_to_int

from .models import Quiz, Question, Choice, Answer, Respondent


class DynamicFieldsModelSerializer(ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class ChoiceSerializer(DynamicFieldsModelSerializer):
    """Список вариантов ответов на вопросы с возможностью выбора"""
    
    question = serializers.SlugRelatedField(queryset=Question.objects.all(), slug_field='question_text')
    
    class Meta:
        model = Choice
        fields = ('question', 'choice_text', 'correct')


    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if not request.user.is_staff:
            data.pop('correct', None)
        return data


class QuestionSerializer(DynamicFieldsModelSerializer):
    """Список вопросов"""

    #choices = ChoiceSerializer(many=True, fields=('choice_text', 'correct'), required=False)
    quiz = serializers.SlugRelatedField(queryset=Quiz.objects.all(), slug_field='name')

    class Meta:
        model = Question
        fields = ('quiz', 'question_text', 'question_type')#, 'choices')

    """
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if data['choices'] == []:
            data.pop('choices', None)
        return data

    def create(self, validated_data):
        choices = validated_data.pop('choices')
        question = Question.objects.create(**validated_data)
        for choice in choices:
            Choice.objects.create(question=question, **choice)
        return question   
    """    


class QuizSerializer(ModelSerializer):
    """Список опросов"""

    #question = QuestionSerializer(many=True, fields=('question_text', 'question_type', 'choices'))

    class Meta:
        model = Quiz
        fields = ('name', 'start_date', 'end_date', 'description')#, 'question')
        validators = []


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('question.choices.question', None)
        return data    


    def update(self, instance, validated_data):
        if instance.start_date !=  validated_data.get('start_date', instance.start_date):
            raise ValidationError({'start_date': 'You must not change date of start quiz'})
        instance.name = validated_data.get('name', instance.name)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

        
    def validate(self, attrs):
        if attrs['start_date'] > attrs['end_date']:
            raise ValidationError(f"Start date must be less or equal end date {attrs['start_date']} > {attrs['end_date']}")
        return attrs       


class AnswerSerializer(ModelSerializer):

    user = serializers.StringRelatedField()
    quiz = serializers.SlugRelatedField(queryset=Quiz.objects.all(), slug_field='name')
    question = serializers.SlugRelatedField(queryset=Question.objects.all(), slug_field='question_text')
    choices = serializers.SlugRelatedField(queryset=Choice.objects.all(), many=True, slug_field='choice_text', required=False)

    class Meta:
        model = Answer
        fields = ('user', 'quiz', 'question', 'choices', 'answer_text')
        read_only_fields = ('user', )
        
    
    def to_representation(self, obj):
        rep = super().to_representation(obj)
        if rep['answer_text'] == "":
            rep['answer_text'] = rep['choices']
        rep.pop('choices', None)
        return rep
   

class QuizPassSerializer(ModelSerializer):

    quiz_answer = serializers.StringRelatedField(many=True)

    class Meta:
        model = Quiz
        fields = ('name', 'quiz_answer')


class RespondentSerializer(ModelSerializer):

    quiz = QuizPassSerializer(many=True)

    class Meta:
        model = Respondent
        fields = ('user', 'session', 'quiz')

    def to_representation(self, obj):
        rep = super().to_representation(obj)
        if rep['user'] is None:
            rep['user'] = 'Anonymous'
        rep.pop('session', None)
        return rep    
