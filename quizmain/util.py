def token_to_int(token, n):
    """
        Convert token to integer value length of n
    """
    import hashlib
    return str(int(hashlib.sha256(token.encode('utf-8')).hexdigest(), 16))[:n]

"""
class RespondentSerializer(serializers.Serializer):

    #quiz = serializers.SlugRelatedField(queryset=Quiz.objects.all(), slug_field='name')
    #answer = serializers.SerializerMethodField()
    #answer_text = serializers.SerializerMethodField()
    #user = serializers.SerializerMethodField()
    #quiz = serializers.SerializerMethodField()
    user = serializers.IntegerField()
    quiz__name = serializers.CharField(max_length=200)
    answers = serializers.CharField(max_length=200)

    #class Meta:
    #    model = Answer
    #    fields = ('user', 'name')#'quiz', 'question', 'choices', 'answer_text')

    
    def get_answers(self, obj):
        quiz = obj.quiz_set.all()
        answers = [] 
        return answers
    #def get_user(self, obj):
        #quizes = Answer.objects.filter()
        #answers = []
        #for quiz in quizes:
            #answers.append({
                #"user": quiz.user,
                #"quiz": quiz,
                #"answers": [answer.choices.values_list('choice_text', flat=True) for answer in Answer.objects.filter(user=obj.user, quiz=obj.quiz)]
        #})
        #return answers


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

 