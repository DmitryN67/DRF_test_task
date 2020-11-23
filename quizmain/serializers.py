from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, RelatedField
from rest_framework.serializers import ValidationError
from rest_framework.serializers import ReadOnlyField
from rest_framework.serializers import SerializerMethodField


from .models import Quiz, Question, Choice, Answer

"""
class QuestionTypeRelatedField(serializers.RelatedField):

    def to_representation(self, value):

        if isinstance(value, AType):
            return 'AType: ' + value.foo
        elif isinstance(value, BType):
            return 'BType: ' + value.bar
        raise Exception('Unexpected type of content_object')
"""

class CurrentUserDefault(object):
    def set_context(self, serializer_field):
        self.user_id = serializer_field.context['request'].user.id

    def __call__(self):
        return self.user_id


class ChoiceSerializer(ModelSerializer):
    """Список вариантов ответов на вопросы с возможностью выбора"""
    
    class Meta:
        model = Choice
        fields = '__all__'

    def to_representation(self, instance):
        rep = super(ChoiceSerializer, self).to_representation(instance)
        request = self.context.get('request')
        if not request.user.is_staff:
            rep.pop('id', None)
            rep.pop('question', None)
            rep.pop('correct', None)
        return rep    


class AnswerSerializer(ModelSerializer):
    """Список ответов"""

    user_id = serializers.IntegerField(default=CurrentUserDefault())

    class Meta:
        model = Answer
        fields = ('user_id', 'question', 'answer_text')

    def to_representation(self, instance):

        #q_id = rep['question']
        #type_field = Question.objects.get(id=q_id).question_type
        #choices = Choice.objects.filter(question__exact=q_id).values_list('choice_text', flat=True)

        rep = super(AnswerSerializer, self).to_representation(instance)
        request = self.context.get('request')
        if rep['user_id'] != request.user.id:
            rep.clear()
        return rep


class QuestionPassSerializer(ModelSerializer):
    """Список вопросов"""

    choices = serializers.StringRelatedField(many=True)
    answer = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ('question_text', 'choices', 'answer')
        read_only_fields = ('question_text', 'choices')
   
    def to_representation(self, instance):
        rep = super(QuestionPassSerializer, self).to_representation(instance)
        request = self.context.get('request')
        if not request.user.is_staff:
            rep.pop('id', None)
            rep.pop('question_type', None)
        if rep['choices'] == []:
            rep.pop('choices', None)
        return rep


class QuestionSerializer(ModelSerializer):
    """Список вопросов"""

    class Meta:
        model = Question
        fields = '__all__'


class QuizSerializer(ModelSerializer):
    """Список опросов"""

    class Meta:
        model = Quiz
        fields = ('id', 'name', 'start_date', 'end_date', 'description')
        validators = []

    def update(self, instance, validated_data):
        if instance.start_date !=  validated_data.get('start_date', instance.start_date):
            raise ValidationError({'start_date': 'Дату начала опроса редактировать нельзя'})
        instance.name = validated_data.get('name', instance.name)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

        
    def validate(self, data):
        request = self.context.get('request')
        if data['start_date'] > data['end_date']:
            raise ValidationError(f"Дата начала опроса больше даты окончания {data['start_date']} > {data['end_date']}")
        return data       


class QuizDetailSerializer(ModelSerializer):

    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ('name', 'start_date', 'end_date', 'description', 'questions')  


class QuizPassSerializer(ModelSerializer):
    """Прохождение опроса"""

    questions = QuestionPassSerializer(many=True)
        
    class Meta:
        model = Quiz
        fields = ('name', 'description', 'questions')
        read_only_fields = ('name', 'description')
