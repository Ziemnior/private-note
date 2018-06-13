from django.shortcuts import render, redirect
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
            request.session['msg_id'] = message_id
            return redirect('note/added')
    else:
        form = CreateMessageForm()
    return render(request, 'index.html', {'form': form})


def note_added_view(request):
    db = dict()
    with create_session() as session:
        for i, x in enumerate(session.scan_iter()):
            db[i] = (x, session.get(x))
        print(db)
    return render(request, 'note.html', {'msg_id': request.session['msg_id'], 'db': db})
