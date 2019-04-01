from django.http import HttpResponse
from .models import Question

def index(request):
    latest_questions = Question.objects.order_by('-pub_date')[:5]
    output = "<br> ".join([str(i+1)+". "+ q.question_text for i, q in enumerate(latest_questions)])
    return HttpResponse("Here are five most recent questions: <br><br>" + output)

def detail(request, question_id):
    response = f"You're looking at question {question_id}."
    return HttpResponse(response)

def results(request, question_id):
    response = f"You're looking at the results of question {question_id}."
    return HttpResponse(response)

def vote(request, question_id):
    response = f"You're voting on question {question_id}."
    return HttpResponse(response)

