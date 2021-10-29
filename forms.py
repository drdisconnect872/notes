from django import forms
from .models import Message


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = {'message','hidden','destroy_hours','destroy_days'}
