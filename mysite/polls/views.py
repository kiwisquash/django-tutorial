from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.utils import timezone

from .models import Question, Choice

def index(request):
    latest_questions = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    # latest_questions = []  
    template = loader.get_template('polls/index.html')
    context = {
        'latest_questions': latest_questions,
    }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    try:
        question = Question.objects.filter(pub_date__lte=timezone.now()).get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist.")
    template = loader.get_template('polls/detail.html')
    context = {
        'question': question,
    }
    return HttpResponse(template.render(context, request))

def results(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist.")
    template = loader.get_template('polls/results.html')
    context = {
        'question': question,
    }
    return HttpResponse(template.render(context, request))

def vote(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist.")

    try:
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        template = loader.get_template('polls/detail.html')
        context = {
            'question': question,
            'error_message': "You did not select a choice.",
        }
        return HttpResponse(template.render(context, request))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args = (question.id,)))
