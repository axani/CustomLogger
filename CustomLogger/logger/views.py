from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.dateparse import parse_datetime

from .models import LogButton, LogEntry
from tokenizer.models import Token

# Create your views here.

def home(request, token):
    messages.info(request, 'Please save this token, to get to your logs: %s' % token)
    return redirect('tokenizer:index')

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
            new_logentry = LogEntry(initiating_button=log_button, token=token)
            new_logentry.save()
            messages.success(request, 'Saved new Log for %s!' % (log_button.name))

            return redirect('tokenizer:token_page', entered_token=token.token)
    return redirect('tokenizer:index')

def edit_logentry(log_id, action, new_date=None):
    log_entry = LogEntry.objects.get(id=log_id)
    if log_entry:
        if action == 'update' and new_date:
            log_entry.date = parse_datetime(new_date)
        elif action == 'delete':
            # Deactivate instead of deleting to give the user the option to undo
            log_entry.active = False
        elif action == 'deactivate':
            log_entry.active = True

        log_entry.save()
        return log_entry
    else:
        return None

def update_log(request, action):
    print(action)
    message_dict = {
        'delete': 'Deleted entry.',
        'update': 'Updated entry.',
    }
    if request.method == "POST":
        log_entry_id = request.POST['log_entry_id']
        date_str = request.POST['log_entry_date']
        log_entry = edit_logentry(log_entry_id, action, new_date=date_str)
        if log_entry:
            token = log_entry.token
            messages.success(request, message_dict[action])
            return redirect('tokenizer:token_page', entered_token=token.token)
    return redirect('tokenizer:index')