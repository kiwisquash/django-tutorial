from django.http import HttpResponse
from django.template import loader

from .models import Question

def index(request):
    latest_questions = Question.objects.order_by('-pub_date')[:5]
    # latest_questions = []  
    template = loader.get_template('polls/index.html')
    context = {
        'latest_questions': latest_questions,
    }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    question = Question.objects.get(pk=question_id)
    template = loader.get_template('polls/detail.html')
    context = {
        'question': question,
    }
    return HttpResponse(template.render(context, request))

def results(request, question_id):
    response = f"You're looking at the results of question {question_id}."
    return HttpResponse(response)

def vote(request, question_id):
    response = f"You're voting on question {question_id}."
    return HttpResponse(response)

