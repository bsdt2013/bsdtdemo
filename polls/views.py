#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import Http404
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from google.appengine.ext import ndb
from polls.models import Poll, Choice
import json


def index(request):
    # Get the data
    latest_poll_list = Poll.query().order(Poll.pub_date).fetch(20)
    return render_to_response('polls/index.html',
                            {'latest_poll_list': latest_poll_list})


def detail(request, poll_key):
    try:
        p = Poll.get_by_id(int(poll_key))
        c = Choice.query(Choice.poll == p.key)
    except:
        raise Http404
    return render_to_response('polls/detail.html',
                            {'poll': p, 'choices': c},
                            context_instance=RequestContext(request))


def results(request, poll_key):
    try:
        p = Poll.get_by_id(int(poll_key))
        c = Choice.query(Choice.poll == p.key)
    except:
        raise Http404
    return render_to_response('polls/results.html', {'poll': p, 'choices': c})


def vote(request, poll_key):
    try:
        p = Poll.get_by_id(int(poll_key))
    except:
        raise Http404
    try:
        selected_choice = Choice.get_by_id(int(request.POST['choice']),
                                            parent=p.key)
        selected_choice.votes += 1
        selected_choice.put()
        return HttpResponseRedirect(reverse('polls.views.results', args=(p.key.id(),)))
    except:
        raise Http404
        # Redisplay the poll voting form.
    #    return render_to_response('polls/detail.html', {
    #        'poll': p,
    #        'error_message': "You didn't select a choice.",
    #    }, context_instance=RequestContext(request))
    #else:

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.


def new(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('polls.views.index'))
    elif request.method == 'POST':
        response_data = {}
        try:
            json_data = json.loads(request.body)
            p = Poll()
            p.title = json_data["title"]
            p.put()
            for choice in json_data["choices"]:
                c = Choice(parent=p.key)
                c.poll = p.key
                c.choice = choice["choice"]
                c.votes = 0
                c.put()
            response_data['result'] = 'success'
            response_data['id'] = p.key.integer_id()
            response_data['title'] = json_data["title"]
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        except:
            response_data['result'] = 'failed'
            response_data['message'] = 'You messed up'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
