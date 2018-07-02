import uuid
from django.shortcuts import render
from random import randint

from .forms import CreateMessageForm
from .redis_utils import create_session
from .ciphering import Ciphering


def index_view(request):
    form = CreateMessageForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            message_id = uuid.uuid5(uuid.NAMESPACE_URL, str(randint(0, 100))).hex
            message_body = form.cleaned_data.get('message_body')
            message_ttl = request.POST['message_ttl']
            msg_body_ciphered = Ciphering.cipher_message(message_id.encode(), message_body)
            with create_session() as session:
                session.rpush(message_id, *msg_body_ciphered)
                session.expire(message_id, message_ttl)
            return render(request, 'note.html', {'msg_id': message_id})
    else:
        form = CreateMessageForm()
    return render(request, 'index.html', {'form': form})


def show_note_view(request, msg_id):
    with create_session() as session:
        msg_body_ciphered = session.lrange(msg_id, 0, -1)
        if not msg_body_ciphered:
            return render(request, 'show_note.html', {'msg_body': 'No such message (Or it was destroyed already)'})
        else:
            if '__confirm__' in request.POST:
                session.delete(msg_id)
                msg_body = Ciphering.decipher_message(msg_id.encode(), msg_body_ciphered)
            else:
                return render(request, 'confirm.html', {})
    return render(request, 'show_note.html', context={'msg_body': msg_body})
