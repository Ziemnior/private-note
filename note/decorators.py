from django.shortcuts import render
from django.utils.functional import wraps
from .redis_utils import create_session


def confirm_required(template_name, context_creator, key='__confirm__'):
    def decorator(func):
        def inner(request, *args, **kwargs):
            if key in request.POST:
                return func(request, *args, **kwargs)
            else:
                return render(request, template_name, {'msg_id': context_creator(kwargs)})
        return wraps(func)(inner)
    return decorator