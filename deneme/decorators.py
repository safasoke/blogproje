from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import reverse


def is_post(func):
    def wrap(request, *args, **kwargs):
        if request.method == 'GET':
            return HttpResponseBadRequest()
        return func(request, *args, **kwargs)

    return wrap


def is_anonymous_required(func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('post-list'))
        return func(request, *args, **kwargs)

    return wrap
