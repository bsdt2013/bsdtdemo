#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from google.appengine.ext import ndb
from polls.models import Poll, Choice


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
    #try:
    p = Poll.get_by_id(int(poll_key))
    #except:
    #    raise Http404

    #try:
        #greeting = Greeting(parent=guestbook_key(guestbook_name))
    #selected_choice = Choice.query(ndb.AND(Choice.id == int(request.POST['choice']),
    #                                        Choice.poll == p.key)).get()
    selected_choice = Choice.get_by_id(int(request.POST['choice']))
    if selected_choice.key.id == int(request.POST['choice']):
        print "lolk"
    #except:
        # Redisplay the poll voting form.
    #    return render_to_response('polls/detail.html', {
    #        'poll': p,
    #        'error_message': "You didn't select a choice.",
    #    }, context_instance=RequestContext(request))
    #else:
    selected_choice.votes += 1
    selected_choice.put()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return HttpResponseRedirect(reverse('polls.views.results', args=(p.key.id(),)))
