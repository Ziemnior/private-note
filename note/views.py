from django.shortcuts import render
from .forms import CreateMessageForm
import uuid
from .redis import create_session
from random import randint


def index_view(request):
    form = CreateMessageForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            message_id = uuid.uuid5(uuid.NAMESPACE_URL, str(randint(0, 100))).hex
            message_body = form.cleaned_data.get('message_body')
            with create_session() as session:
                session.set(message_id, message_body)
            return render(request, 'note.html', {'msg_id': message_id})
    else:
        form = CreateMessageForm()
    return render(request, 'index.html', {'form': form})


def note_show_view(request, msg_id):
    with create_session() as session:
        msg_body = session.get(msg_id).decode('utf-8')
        return render(request, 'show_note.html', {'msg_body': msg_body})
