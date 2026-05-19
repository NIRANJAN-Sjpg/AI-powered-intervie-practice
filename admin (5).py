from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db.models import Avg
from .models import Question, InterviewAttempt, Feedback
from .serializers import QuestionSerializer, AttemptSerializer, SubmitAttemptSerializer
from .gemini_service import evaluate_answer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def question_list(request):
    """Return questions filtered by role and/or difficulty."""
    role = request.query_params.get('role', None)
    difficulty = request.query_params.get('difficulty', None)

    qs = Question.objects.all()
    if role:
        qs = qs.filter(role=role)
    if difficulty:
        qs = qs.filter(difficulty=difficulty)

    serializer = QuestionSerializer(qs.order_by('?')[:10], many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_attempt(request):
    """Receive transcript, call Gemini, save and return feedback."""
    serializer = SubmitAttemptSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    question_id = serializer.validated_data['question_id']
    transcript = serializer.validated_data['transcript']

    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return Response({'error': 'Question not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Save the attempt
    attempt = InterviewAttempt.objects.create(
        user=request.user,
        question=question,
        transcript=transcript,
    )

    # Call Gemini
    try:
        result = evaluate_answer(
            question_text=question.text,
            transcript=transcript,
            ideal_answer=question.ideal_answer,
            role=question.get_role_display(),
        )
    except Exception as e:
        attempt.delete()
        return Response({'error': f'AI evaluation failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Save feedback
    Feedback.objects.create(
        attempt=attempt,
        clarity_score=result.get('clarity_score', 0),
        content_score=result.get('content_score', 0),
        confidence_score=result.get('confidence_score', 0),
        overall_score=result.get('overall_score', 0),
        strengths=result.get('strengths', []),
        improvements=result.get('improvements', []),
        model_answer=result.get('model_answer', ''),
    )

    return Response(AttemptSerializer(attempt).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attempt_list(request):
    """Return all attempts by the logged-in user."""
    attempts = InterviewAttempt.objects.filter(user=request.user).order_by('-created_at')
    return Response(AttemptSerializer(attempts, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attempt_detail(request, pk):
    """Return a single attempt detail."""
    try:
        attempt = InterviewAttempt.objects.get(id=pk, user=request.user)
    except InterviewAttempt.DoesNotExist:
        return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    return Response(AttemptSerializer(attempt).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stats(request):
    """Return aggregated stats for the user's progress dashboard."""
    attempts = InterviewAttempt.objects.filter(user=request.user).prefetch_related('feedback')
    total = attempts.count()

    if total == 0:
        return Response({
            'total_attempts': 0,
            'avg_overall': 0,
            'avg_clarity': 0,
            'avg_content': 0,
            'avg_confidence': 0,
            'recent': [],
        })

    agg = attempts.aggregate(
        avg_overall=Avg('feedback__overall_score'),
        avg_clarity=Avg('feedback__clarity_score'),
        avg_content=Avg('feedback__content_score'),
        avg_confidence=Avg('feedback__confidence_score'),
    )

    recent = attempts.order_by('-created_at')[:5]
    recent_data = []
    for a in recent:
        if hasattr(a, 'feedback'):
            recent_data.append({
                'id': a.id,
                'question': a.question.text[:60],
                'role': a.question.role,
                'overall_score': a.feedback.overall_score,
                'created_at': a.created_at,
            })

    return Response({
        'total_attempts': total,
        'avg_overall': round(agg['avg_overall'] or 0, 1),
        'avg_clarity': round(agg['avg_clarity'] or 0, 1),
        'avg_content': round(agg['avg_content'] or 0, 1),
        'avg_confidence': round(agg['avg_confidence'] or 0, 1),
        'recent': recent_data,
    })
