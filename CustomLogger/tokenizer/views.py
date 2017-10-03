from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from .models import Token

# Create your views here.
def index(request):
    return render(request, 'tokenizer/index.html')

def token_page(request, entered_token):
    token = get_object_or_404(Token, token=entered_token)

    return render(request, 'tokenizer/token_page.html', {'token': entered_token})