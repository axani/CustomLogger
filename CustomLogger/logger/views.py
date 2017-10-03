from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import LogButton
from tokenizer.models import Token

# Create your views here.

def add_log_button(request):
    if request.method == "POST":
        token_id = request.POST['token_id']
        new_button = request.POST['button_name']
        token = Token.objects.get(id=token_id)
        if token:
            new_log_button = LogButton(name=new_button, token=token)
            new_log_button.save()
            messages.success(request, 'Added a new button :-)')

            # Redirect to token page
            # Because the user should be able to copy the token out of the browser
            return redirect('tokenizer:token_page', entered_token=token.token)
    return redirect('tokenizer:index')

def log(request):
    if request.method == "POST":
        log_button_id = request.POST['log_button_id']
        log_button = LogButton.objects.get(id=log_button_id)
        if log_button:
            token = log_button.token
            messages.success(request, 'LOGGED!')

            return redirect('tokenizer:token_page', entered_token=token.token)
    return redirect('tokenizer:index')