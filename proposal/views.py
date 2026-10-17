import json
import unicodedata
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Question, Response

# The name she has to enter on the first slide (case, accents and extra spaces are ignored).
FIRST_NAME = 'Celia'
LAST_NAME = 'Palafox'


def normalize(text):
    text = unicodedata.normalize('NFKD', str(text))
    text = ''.join(c for c in text if not unicodedata.combining(c))
    return ' '.join(text.split()).casefold()


def read_json(request):
    try:
        return json.loads(request.body)
    except (ValueError, TypeError):
        return {}


def proposal(request):
    questions = [
        {'id': q.id, 'prompt': q.prompt, 'choices': q.choice_list()}
        for q in Question.objects.all()
    ]
    return render(request, 'proposal/proposal.html', {'questions': questions})


@require_POST
def check_name(request):
    data = read_json(request)
    ok = (
        normalize(data.get('first', '')) == normalize(FIRST_NAME)
        and normalize(data.get('last', '')) == normalize(LAST_NAME)
    )
    if ok:
        request.session['proposal_name_ok'] = True
    return JsonResponse({'ok': ok})


@require_POST
def check_answer(request, question_id):
    if not request.session.get('proposal_name_ok'):
        return JsonResponse({'ok': False, 'hint': 'Tell me who you are first 👀'}, status=403)

    question = get_object_or_404(Question, id=question_id)
    answer = normalize(read_json(request).get('answer', ''))
    if answer not in {normalize(a) for a in question.answer_list()}:
        return JsonResponse({'ok': False, 'hint': question.hint})

    return JsonResponse({
        'ok': True,
        'image': question.image.build_url(secure=True) if question.image else '',
        'caption': question.caption,
    })


@require_POST
def final_answer(request):
    data = read_json(request)
    try:
        no_attempts = max(0, int(data.get('no_attempts', 0)))
    except (TypeError, ValueError):
        no_attempts = 0
    Response.objects.create(answer=str(data.get('answer', 'yes'))[:10], no_attempts=no_attempts)
    return JsonResponse({'ok': True})
