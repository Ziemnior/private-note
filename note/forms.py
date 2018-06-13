from django import forms
from django.forms.widgets import Textarea


class CreateMessageForm(forms.Form):
    message_body = forms.CharField(widget=Textarea)

    def clean(self, *args, **kwargs):
        message_body = self.cleaned_data.get('message_body')
        if not message_body:
            raise forms.ValidationError('Enter message')
        return super(CreateMessageForm, self).clean(*args, **kwargs)
