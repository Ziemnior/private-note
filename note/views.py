from django.shortcuts import render
from .forms import CreateMessageForm
import uuid
from .redis import create_session


def index_view(request):
    form = CreateMessageForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            message_id = uuid.uuid4().hex
            message_body = form.cleaned_data['message_body']
            with create_session() as session:
                session.set(message_id, message_body)

    # just for debug purposes
    db = dict()
    with create_session() as session:
        for i, x in enumerate(session.scan_iter()):
            db[i] = (x, session.get(x))
        print(db)

    return render(request, 'index.html', {'db': db})
