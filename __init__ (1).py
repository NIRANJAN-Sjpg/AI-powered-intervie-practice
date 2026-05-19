from rest_framework import serializers
from .models import Question, InterviewAttempt, Feedback


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'text', 'role', 'difficulty')


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = (
            'clarity_score', 'content_score', 'confidence_score',
            'overall_score', 'strengths', 'improvements', 'model_answer'
        )


class AttemptSerializer(serializers.ModelSerializer):
    feedback = FeedbackSerializer(read_only=True)
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = InterviewAttempt
        fields = ('id', 'question', 'transcript', 'created_at', 'feedback')


class SubmitAttemptSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    transcript = serializers.CharField(min_length=10)
