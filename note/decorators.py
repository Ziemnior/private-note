from django.shortcuts import render
from django.utils.functional import wraps
from .redis_utils import create_session


def confirm_required(template_name, key='__confirm__'):
    def decorator(func):
        def inner(request, *args, **kwargs):
            with create_session() as session:
                if not session.lrange(kwargs['msg_id'], 0, -1):
                    return render(request, 'show_note.html', {'msg_body': 'No such message (Or it was destroyed already)'})
                else:
                    if key in request.POST:
                        return func(request, *args, **kwargs)
                    else:
                        return render(request, template_name, {})
        return wraps(func)(inner)
    return decorator
