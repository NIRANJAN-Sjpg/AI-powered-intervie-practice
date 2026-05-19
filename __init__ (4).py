from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    ROLE_CHOICES = [
        ('software', 'Software Engineer'),
        ('bpo', 'BPO / Customer Support'),
        ('data', 'Data Analyst'),
        ('hr', 'HR Round'),
    ]
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    text = models.TextField()
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='easy')
    ideal_answer = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.role}] {self.text[:60]}"


class InterviewAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempts')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='attempts')
    transcript = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.question.text[:40]} - {self.created_at.date()}"


class Feedback(models.Model):
    attempt = models.OneToOneField(InterviewAttempt, on_delete=models.CASCADE, related_name='feedback')
    clarity_score = models.IntegerField(default=0)
    content_score = models.IntegerField(default=0)
    confidence_score = models.IntegerField(default=0)
    overall_score = models.IntegerField(default=0)
    strengths = models.JSONField(default=list)
    improvements = models.JSONField(default=list)
    model_answer = models.TextField(blank=True)

    def __str__(self):
        return f"Feedback for attempt #{self.attempt.id} — overall: {self.overall_score}/10"
