# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Question
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Choice
from django.views import generic
from django.utils import timezone

'''
def index(request):
    latest_quest_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list':latest_quest_list}
    return render(request,'stonepolls/index.html',context)

def detail(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    return render(request,'stonepolls/detail.html',{'question':question})

def results(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    return render(request,'stonepolls/results.html',{'question':question})

'''

def vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(request,"stonepolls/detail.html",
                      {'question':question,
                       'error_message':'you did not select a choice'
                       }
                      )
    else:
        selected_choice.vote += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('stonepolls:results', args=(question.id,)))


class IndexView(generic.ListView):
    template_name = 'stonepolls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'stonepolls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that are not published yet.
        """
        return  Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'stonepolls/results.html'



