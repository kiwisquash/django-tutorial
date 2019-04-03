from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

from .models import Question, Choice

def index(request):
    latest_questions = Question.objects.order_by('-pub_date')[:5]
    # latest_questions = []  
    template_dir = 'polls/index.html'
    context = {
        'latest_questions': latest_questions,
    }
    return render(request, template_dir, context)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist.")
    template_dir = 'polls/detail.html'
    context = {
        'question': question,
    }
    return render(request, template_dir, context)

def results(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist.")
    template_dir = 'polls/results.html'
    context = {
        'question': question,
    }
    return render(request, template_dir, context)

def vote(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist.")

    try:
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        template_dir = 'polls/detail.html'
        context = {
            'question': question,
            'error_message': "You did not select a choice.",
        }
        return render(request, template_dir, context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args = (question.id,)))
