import json
import os
import google.generativeai as genai
from django.conf import settings


def evaluate_answer(question_text, transcript, ideal_answer, role):
    """
    Calls Gemini 1.5 Flash (free tier) to evaluate an interview answer.
    Returns a dict with scores and feedback.
    """
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in your .env file.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""You are an expert interview coach evaluating a fresher candidate's spoken answer.

Job Role: {role}
Interview Question: {question_text}
Candidate's Answer (transcribed from speech): {transcript}
Ideal Answer Reference: {ideal_answer}

Evaluate the candidate's answer and respond ONLY with a valid JSON object.
Do NOT include markdown backticks or any extra text — just raw JSON.

{{
  "clarity_score": <integer 0-10>,
  "content_score": <integer 0-10>,
  "confidence_score": <integer 0-10>,
  "overall_score": <integer 0-10>,
  "strengths": ["specific strength 1", "specific strength 2"],
  "improvements": ["specific improvement 1", "specific improvement 2"],
  "model_answer": "A complete model answer the candidate can learn from"
}}

Scoring guide:
- clarity_score: Was the answer easy to understand? Clear structure?
- content_score: Was the information accurate and complete?
- confidence_score: Did the answer sound confident and well-structured?
- overall_score: Holistic impression of the answer"""

    response = model.generate_content(prompt)
    raw = response.text.strip()

    # Clean up if Gemini wraps in markdown
    if raw.startswith('```'):
        lines = raw.split('\n')
        raw = '\n'.join(lines[1:-1])
    raw = raw.strip()

    return json.loads(raw)
