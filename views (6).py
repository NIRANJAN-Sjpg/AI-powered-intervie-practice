from django.urls import path
from . import views

urlpatterns = [
    path('questions/', views.question_list, name='question-list'),
    path('attempts/', views.attempt_list, name='attempt-list'),
    path('attempts/submit/', views.submit_attempt, name='submit-attempt'),
    path('attempts/<int:pk>/', views.attempt_detail, name='attempt-detail'),
    path('stats/', views.stats, name='stats'),
]
