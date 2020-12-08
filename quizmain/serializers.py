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

    choices = ChoiceSerializer(many=True, fields=('choice_text', 'correct'), required=False)
    quiz = serializers.SlugRelatedField(queryset=Quiz.objects.all(), slug_field='name')

    class Meta:
        model = Question
        fields = ('quiz', 'question_text', 'question_type', 'choices')

    
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


class QuizSerializer(ModelSerializer):
    """Список опросов"""

    question = QuestionSerializer(many=True, fields=('question_text', 'question_type', 'choices'))

    class Meta:
        model = Quiz
        fields = ('name', 'start_date', 'end_date', 'description', 'question')
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

        
    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise ValidationError(f"Start date must be less or equal end date {data['start_date']} > {data['end_date']}")
        return data       


class AnswerSerializer(ModelSerializer):

    user = serializers.StringRelatedField()
    quiz = serializers.SlugRelatedField(queryset=Quiz.objects.all(), slug_field='name')
    question = serializers.SlugRelatedField(queryset=Question.objects.all(), slug_field='question_text')
    choices = serializers.SlugRelatedField(queryset=Choice.objects.all(), many=True, slug_field='choice_text', required=False)
    
    class Meta:
        model = Answer
        fields = ('user', 'quiz', 'question', 'choices', 'answer_text')
        read_only_fields = ('user', )
        #validators = []

    #def get_user(self, obj):
        #if obj.user is None:
            #return 'Anonymous'
        #return obj.user
            
    
    def to_representation(self, obj):
        rep = super().to_representation(obj)
        if rep['answer_text'] == "":
            rep['answer_text'] = rep['choices']
        rep.pop('choices', None)
        return rep
    """
    def create(self, validated_data):
        #raise ValidationError(f"Данные - {validated_data}")
        choices = validated_data.pop('choices')
        answers = self.data['choices']
        #answer = validated_data['answer_text']
        obj = Answer.objects.create(**validated_data)
        if 'answer_text' not in validated_data.keys():
            #answers = [choice for choice in choices]
            #raise ValidationError(f"Данные - {answers}")
            obj.save(answer_text=answers)
            for choice, value in choices.items():
                field = getattr(obj, choice)
                field.set(value)
        else:    
            obj.save()    
        return obj

    def validate_answer_text(self, value):
        raise ValidationError(f"Данные - {value}")
        if not value:
            return self.data['choices']

          

    def validate(self, data):
        #raise ValidationError(f"Данные - {data}")
        if self.is_valid():
            if data['answer_text'] == "":
                data['answer_text'] = self.data['choices']
            #raise serializers.ValidationError("finish must occur after start")
        return data        
"""            
            

class QuizPassSerializer(ModelSerializer):

    quiz_answer = serializers.StringRelatedField(many=True)

    class Meta:
        model = Quiz
        fields = ('name', 'quiz_answer')


class UserSerializer(ModelSerializer):

    user = serializers.SerializerMethodField()
    #session = serializers.PrimaryKeyRelatedField(read_only=True)
    #quiz = 
    #session_answers = serializers.SlugRelatedField(many=True, slug_field='answer_text', read_only=True)

    class Meta:
        model = Answer
        fields = ('user', 'answer_text')
        read_only_fields = ('user',)


    def get_user(self, obj):
        session = Answer.objects.get(session=obj.session)
        uid = session.get_decoded().get('_auth_user_id')
        try:
            user = User.objects.get(pk=uid).username
        except:
            user = 'Anonymous'    
        return user
    
    def to_representation(self, obj):
        rep = super().to_representation(obj)
        rep.pop('session_key', None)
        return rep


class RespondentSerializer(ModelSerializer):
#class RespondentSerializer(serializers.Serializer):

    #quiz = serializers.SlugRelatedField(queryset=Quiz.objects.all(), slug_field='name')
    #quiz = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    #answer = serializers.SerializerMethodField()
    #user = serializers.SerializerMethodField()
    #quiz = QuizSerializer(read_only=True, many=True)
    quiz = QuizPassSerializer(many=True)
    #answer_text = serializers.SerializerMethodField()
    
    
    #user = serializers.IntegerField()
    #quiz = serializers.CharField(max_length=200)
    #answers = serializers.CharField(max_length=200)

    class Meta:
        model = Respondent
        fields = ('user', 'session', 'quiz')
        read_only_fields = ('user', 'session', 'quiz')

    #def get_user(self, obj):
        #users = Answer.objects.values('user').distinct()
        ##raise ValidationError(f"Пользователи - {users}")
        #return users
"""
    def get_answer_text(self, obj):
        answers = Answer.objects.filter(user=obj.id).values('answer_text')
        return answers

    def get_quiz(self, obj):
        quizes = Quiz.objects.filter(quiz_respondent=obj.id).values('name').annotate(answers=F(self.get_answer_text(obj)))
        return quizes
#

    
    def get_quiz(self, obj):
        quizes = Quiz.objects.filter(quiz_answer=obj.quiz).values('quiz')
        return quizes


    def to_representation (self, instance):  
        rep = super().to_representation(instance)
        if rep['answer_text'] == "":
            rep['answer_text'] = rep['choices']
        rep.pop('choices', None)
        answers = [instance.choices.values_list('choice_text', flat=True) for instance in Answer.objects.filter(user=instance.user, quiz=instance.quiz)]
        rep['quiz'] = {quiz.name: answers for quiz in Quiz.objects.filter(name=instance.quiz)}
        rep.pop('answer_text', None)
        #raise ValidationError(f"Ответы - {answers}")
        return rep

    def to_representation(self, obj):
        return {"user": obj.user,
                "quiz": {"name": obj.quiz.name, "slug": obj.job.slug, 
             "title": obj.job.seo_title}
                }    
"""                