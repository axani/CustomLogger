from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404
from django.conf import settings
from django.contrib import messages
from django.utils import timezone

from random import choice
from string import ascii_lowercase
from .models import Token
from logger.models import LogButton, LogEntry


# Create your views here.
def index(request):
    # messages.success(request, 'Hello!')
    return render(request, 'tokenizer/index.html')

def token_page(request, entered_token, additional_content={}):
    token = get_object_or_404(Token, token=entered_token)
    #return render(request, 'tokenizer/token_page.html', {'token': entered_token})
    # Use Logger App from here
    # TODO: This really has nothing to do with tokenizer anymore.
    # Put this to logger views!

    content = additional_content
    content['token'] = token
    content['data'] = {
            'user_timezone': token.timezone,
            'log_buttons': LogButton.objects.filter(token=token, active=True),
            'log_entries': LogEntry.objects.filter(token=token, active=True)
        }
    return render(request, 'logger/index.html', content)

def create_token(request):
    def getRandomString():
        length = Token._meta.get_field('token').max_length
        letters = ascii_lowercase
        return ''.join([choice(letters) for _ in range(length)])

    def getTimezone(request):
        if request.method == "POST":
            user_timezone = request.POST['user_timezone']
            try:
                # User may have a corrupted timezone so test it first
                timezone.activate(user_timezone)
                return user_timezone
            except:
                return settings.TIME_ZONE
        else:
            return settings.TIME_ZONE

    generated_token = getRandomString()
    while Token.objects.filter(token=generated_token).exists():
        generated_token = getRandomString()
    new_token = Token(token=generated_token)
    new_token.timezone = getTimezone(request)
    new_token.save()
    messages.success(request, 'Unique token page created.')
    return redirect('tokenizer:token_page', entered_token=new_token)