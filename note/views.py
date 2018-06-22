import uuid
from django.shortcuts import render
from random import randint

from .forms import CreateMessageForm
from .redis_utils import create_session
from .ciphering import Ciphering
from .decorators import confirm_required


def index_view(request):
    form = CreateMessageForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            message_id = uuid.uuid5(uuid.NAMESPACE_URL, str(randint(0, 100))).hex
            message_body = form.cleaned_data.get('message_body')
            msg_body_ciphered = Ciphering.cipher_message(message_id.encode(), message_body)
            with create_session() as session:
                session.rpush(message_id, *msg_body_ciphered)
            return render(request, 'note.html', {'msg_id': message_id})
    else:
        form = CreateMessageForm()
    return render(request, 'index.html', {'form': form})


def confirmation_context_helper(context):
    with create_session() as session:
        message = session.lrange(context['msg_id'], 0, -1)
        return True if message else None


@confirm_required('confirm.html', confirmation_context_helper)
def show_note_view(request, msg_id):
    with create_session() as session:
        msg_body_ciphered = session.lrange(msg_id, 0, -1)
        try:
            msg_body_ciphered[0]
        except IndexError:
            msg_body = 'message was destroyed already'
        else:
            session.delete(msg_id)
            msg_body = Ciphering.decipher_message(msg_id.encode(), msg_body_ciphered)
        finally:
            return render(request, 'show_note.html', context={'msg_body': msg_body})
