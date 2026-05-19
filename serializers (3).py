from django.contrib import admin
from .models import Question, InterviewAttempt, Feedback


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'role', 'difficulty')
    list_filter = ('role', 'difficulty')
    search_fields = ('text',)


@admin.register(InterviewAttempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'created_at')
    list_filter = ('created_at',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'overall_score', 'clarity_score', 'content_score', 'confidence_score')
