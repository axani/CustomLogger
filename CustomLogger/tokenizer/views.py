from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404
from django.contrib import messages
from random import choice
from string import ascii_lowercase
from .models import Token
from logger.models import LogButton, LogEntry


# Create your views here.
def index(request):
    messages.success(request, 'Hello!')
    return render(request, 'tokenizer/index.html')

def token_page(request, entered_token):
    token = get_object_or_404(Token, token=entered_token)
    #return render(request, 'tokenizer/token_page.html', {'token': entered_token})
    # Use Logger App from here
    content = {
        'token': token,
        'data': {
            'log_buttons': LogButton.objects.filter(token=token),
            'log_entries': LogEntry.objects.filter(token=token)
        }
    }
    return render(request, 'logger/index.html', content)

def create_token(request):
    def getRandomString():
        length = Token._meta.get_field('token').max_length
        letters = ascii_lowercase
        return ''.join([choice(letters) for _ in range(length)])
    generated_token = getRandomString()
    while Token.objects.filter(token=generated_token).exists():
        generated_token = getRandomString()
    new_token = Token(token=generated_token)
    new_token.save()
    messages.success(request, 'Unique token page created.')
    return redirect('tokenizer:token_page', entered_token=new_token)