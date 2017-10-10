from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.dateparse import parse_datetime
from django.conf import settings
from django.utils import timezone

from datetime import datetime

from .models import LogButton, LogEntry
from tokenizer.models import Token
from tokenizer.views import token_page


# Create your views here.

def _getCompleteTokenURL(request, token):
    scheme = request.scheme + '://' # http or https
    host = request.get_host()
    subdomain = settings.TOKEN_SUBDOMAIN
    return scheme + '/'.join([host, subdomain, token])

def _clear_session(request):
    # Don't show undo link all the time
    if 'undo_link' in request.session.keys():
        del request.session['undo_link']
    return request

def home(request, token):
    print( request.build_absolute_uri())

    this_url = _getCompleteTokenURL(request, token)
    messages.info(request, 'Please save this token, to get to your logs:<br> <a href="%s">%s</a>' % (this_url, this_url), extra_tags='safe')
    return redirect('tokenizer:index')

def add(request, target_type):
    request = _clear_session(request)
    if request.method == "POST":
        token_id = request.POST['token_id']
        token = Token.objects.get(id=token_id)
        if token:
            if target_type == 'button':
                new_button = request.POST['button_name']
                new_log_button = LogButton(name=new_button, token=token)
                new_log_button.save()
                messages.success(request, 'Added new log button: "%s"' % (new_button))
            if target_type == 'log':
                log_button_id = request.POST['log_button_id']
                log_button = LogButton.objects.get(id=log_button_id)
                if log_button:
                    timezone.activate(token.timezone)
                    date = timezone.localtime()
                    print(token.timezone)
                    print(date)
                    new_logentry = LogEntry(initiating_button=log_button, token=token, date=date)
                    new_logentry.save()
                    nice_date = str(date)[:16]
                    messages.success(request, 'Added new log for %s: "%s"' % (log_button.name, nice_date))

            # Redirect to token page
            # Because the user should be able to copy the token out of the browser
            return redirect('tokenizer:token_page', entered_token=token.token)
    return redirect('tokenizer:index')

def update(request, action, target_type, target_id):
    request = _clear_session(request)

    print(action)

    message_dict = {
        'delete': 'Deleted %s.' % target_type,
        'update': 'Updated %s.' % target_type,
        'undo': 'Reverted changes on %s.' % target_type,
    }
    if target_type == 'log':
        if request.method == "POST":
            if 'log_entry_date' in request.POST:
                date_str = request.POST['log_entry_date']
                target = _edit_logentry(target_id, action, new_date=date_str)
            else:
                target = _edit_logentry(target_id, action)
        else:
            target = _edit_logentry(target_id, action)
    if target_type == 'button':
        # TODO: Merge with target_type = 'log' part
        if request.method == "POST":
            if 'button_name' in request.POST:
                new_button_name = request.POST['button_name']
                target = _edit_button(target_id, action, new_name=new_button_name)
            else:
                target = _edit_button(target_id, action)
        else:
            target = _edit_button(target_id, action)
    if target:
        token = target.token
        messages.success(request, message_dict[action])
        if action == 'delete':
            request.session['undo_link'] = reverse('logger:update', kwargs={'action': 'undo', 'target_type': target_type, 'target_id': target_id})
        return redirect('tokenizer:token_page', entered_token= token.token)
    return redirect('tokenizer:index')

def _edit_logentry(log_id, action, new_date=None):
    log_entry = LogEntry.objects.get(id=log_id)
    if log_entry:
        if action == 'update' and new_date:
            log_entry.date = parse_datetime(new_date)
        elif action == 'delete':
            # Deactivate instead of deleting to give the user the option to undo
            log_entry.active = False
        elif action == 'undo':
            log_entry.active = True

        log_entry.save()
        return log_entry
    else:
        return None

def _edit_button(button_id, action, new_name=None):
    # TODO: Merge this with _edit_logentry
    this_button = LogButton.objects.get(id=button_id)
    if this_button:
        if action == 'update' and new_name:
            this_button.name = new_name
        elif action == 'delete':
            # Deactivate instead of deleting to give the user the option to undo
            this_button.active = False
        elif action == 'undo':
            this_button.active = True

        this_button.save()
        return this_button
    else:
        return None
