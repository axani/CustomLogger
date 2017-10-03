from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from .models import Token
from random import choice
from string import ascii_lowercase

# Create your views here.
def index(request):
    return render(request, 'tokenizer/index.html')

def token_page(request, entered_token):
    token = get_object_or_404(Token, token=entered_token)
    return render(request, 'tokenizer/token_page.html', {'token': entered_token})

def create_token(request):
    length = Token._meta.get_field('token').max_length
    letters = ascii_lowercase
    generated_token = ''.join([choice(letters) for _ in range(length)])
    new_token = generated_token
    return render(request, 'tokenizer/token_page.html', {'token': new_token})