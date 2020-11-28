from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, RelatedField
from rest_framework.serializers import ValidationError
from rest_framework.serializers import ReadOnlyField
from rest_framework.serializers import SerializerMethodField
from django.contrib.auth.models import User

from .util import token_to_int

from .models import Quiz, Question, Choice, Answer


class DynamicTypeRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        """
        Serialize objects to a simple textual representation.
        """
        if value == 'one':
            return serializers.CharField
        elif value == 'choose_one':
            return serializers.ChoiceField
        else:
            return serializers.MultipleChoiceField    
        raise Exception(f'Занчение {value} недопустимо')


class DynamicFieldsModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class ChoicePrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def display_value(self, instance):
        return f"{instance.choice_text}"


class CurrentUserDefault(object):
    #def set_context(self, serializer_field):
        #self.user_id = serializer_field.context['request'].user.id
#
    #def __call__(self):
        #return self.user_id


    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['request'].user


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


class QuestionSerializer(ModelSerializer):
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

    
class QuestionPassSerializer(ModelSerializer):
    """Список вопросов"""

    #choice = serializers.SlugRelatedField(many=True, slug_field='choice_text', read_only=True)
    
    class Meta:
        model = Question
        fields = ('quiz', 'question_text', 'choice')


class QuizSerializer(ModelSerializer):
    """Список опросов"""

    question = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ('name', 'start_date', 'end_date', 'description', 'question')
        validators = []

    #def get_question(self, obj):
        #questions = Question.objects.filter(quiz=obj)
        #serializer = QuestionSerializer(instance=questions, many=True)
        #return serializer.data

    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        #request = self.context.get('request')
        #raise ValidationError({f"Данные - {data}, запрос - {request}"})
        #if not request.user.is_staff:
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


class UserSerializer(serializers.ModelSerializer):
    
    user_answer = serializers.SlugRelatedField(many=True, read_only=True, slug_field='answer_text')
    #user_answer = QuizSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'user_answer']


class AnswerSerializer(ModelSerializer):

    #user = serializers.ReadOnlyField(source='user.username' )
    #question = QuestionSerializer()
    #question = serializers.SerializerMethodField()

    #choices = serializers.SlugRelatedField(queryset=Choice.objects.all(), many=True, slug_field='choice_text', required=False)
    
    #choices = ChoiceSerializer(many=True)
    #choices = serializers.SerializerMethodField()
    
    class Meta:
        model = Answer
        fields = ('user', 'question', 'choices', 'answer_text')
        read_only_fields = ('user', )


    #def get_question(self, obj):
    #    questions = Question.objects.filter(quiz=obj)
    #    serializer = QuestionSerializer(instance=questions, many=True)
    #    return serializer.data        


    def to_representation(self, instance):
        request = self.context.get('request')
        data = super().to_representation(instance)
        #raise ValidationError(f"Данные - {request.user.id}, запрос - {token_to_int(request.COOKIES['csrftoken'], 8)}")
        #raise ValidationError(f"Данные - {data}, запрос - {request}")
        question_type = Question.objects.get(pk=data['question'])
        if question_type == 'text':
            data.pop('choices', None)
        #choices = Choice.objects.filter(question__exact=data['question']).values_list('choice_text', flat=True)
        #data['choices'] = Choice.objects.filter(question__exact=data['question']).values_list('choice_text', flat=True)
        #raise ValidationError(f"Тип вопроса - {question_type}, варианты - {data['choices']}")
        if question_type in ['choose_one', 'choose_many']:
            
            self.fields['answer_text'] = self.fields['choices']
        #try:
            #del self._readable_fields
        #except AttributeError:
            #pass
        return data
    """
    def validate(self, attrs):
        question_type = Question.objects.get(pk=attrs['question'].id).question_type
        raise ValidationError(f"Тип вопроса - {question_type}")
        try:
            if question_type == "choose_one" or question_type == "text":
                obj = Answer.objects.get(question=attrs['question'].id, user=attrs['user'])
            elif question_type == "choose_many":
                obj = Answer.objects.get(question=attrs['question'].id, userd=attrs['user'], choices=attrs['choices'])
        except Answer.DoesNotExist:
            return attrs
        else:
            raise serializers.ValidationError('Already responded')

    
    def validate_answer_text(self, value):
        #question_type = Question.objects.get(pk=attrs['question'].id).question_type
        question_type = self.fields['question']
        #choices = Choice.objects.filter(question__exact=attrs['question'].id).values_list('choice_text', flat=True)
        #choices = Choice.objects.filter(question__exact=self.fields['question'].id).values_list('choice_text', flat=True)
        #raise ValidationError(f"Тип вопроса - {question_type}, варианты - {1}")
        if question_type == "choose_one":
            #raise ValidationError(f"Ответ - {attrs['answer_text']}, варианты - {choices}")
            if self.fields['answer_text'] not in choices:
                serializers.ValidationError('Answer must be in list of choice') 
            if len(attrs['answer_text'] > 1):
                serializers.ValidationError('Answer must be one of item of choice')  
        elif question_type == "choose_many":
            if attrs['answer_text'] not in choices:
                serializers.ValidationError('Answer must be in list of choice') 
        return value
    """    
    

    """
    def save(self):
        user = self.validated_data['user']
        question = self.validated_data['question']
        choices = self.validated_data['choices']
        answer_text = self.validated_data['answer_text']
        answer = self.data['answer_text']
        user = self.data['user']
        for question in answers:
            question_id = Question.objects.get(pk=self.data['question']).id
            choices = answers[question_id]
            for choice_id in choices:
                choice = Choice.objects.get(pk=choice_id)
                Answer(user=user, question=question, choices=choice).save()
                user.save()             
    """

"""
class AnswerSerializer(serializers.Serializer):
    
    user_id = serializers.IntegerField(default=CurrentUserDefault())
    answers = serializers.JSONField()

    def validate_answers(self, answers):
        if not answers:
            raise ValidationError("Поле ответа не может быть пустым")
        return answers

    def save(self):
        answers = self.data['answers']
        user = self.context.user_id
        for question_id in answers:
            question = Question.objects.get(pk=question_id)
            choices = answers[question_id]
            for choice_id in choices:
                choice = Choice.objects.get(pk=choice_id)
                Answer(user_id=user, question=question, choice=choice).save()
                user.is_answer = True
                user.save()        
"""        
