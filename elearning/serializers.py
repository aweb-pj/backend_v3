from rest_framework import serializers
from elearning.models import *


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ('answer','question')


class HomeworkAnswerSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = HomeworkAnswer
        fields = ('answers','student','node_homework')

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        homework_answer = HomeworkAnswer.objects.create(**validated_data)
        for answer_data in answers_data:
            Answer.objects.create(homework_answer=homework_answer, **answer_data)
        return homework_answer


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('id','type','question','A','B','C','D','correct_answer','order')
        read_only_fields = ('id',)


class NodeHomeworkSerializer(serializers.ModelSerializer):

    questions = QuestionSerializer(many=True)

    class Meta:
        model = NodeHomework
        fields = ('questions','published','node_id')

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        node_homework = NodeHomework.objects.create(**validated_data)
        for question_data in questions_data:
            Question.objects.create(node_homework=node_homework, **question_data)
        return node_homework


class MaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Material
        fields = ('id','material_file')
        read_only_fields = ('id',)


class NodeMaterialSerializer(serializers.ModelSerializer):

    materials = MaterialSerializer(many=True,read_only=True)

    class Meta:
        model = NodeMaterial
        fields = ('materials','id')
        read_only_fields = ('id',)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','name','role')
        read_only_fields = ('id',)

