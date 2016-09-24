import httplib2
from datetime import datetime
from django.shortcuts import render, reverse, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from apiclient.discovery import build
from oauth2client.client import AccessTokenCredentials

from .models import Events
# Create your views here.


@login_required(login_url='login')
def home(request):
    context = {}
    if request.user.social_auth.get(provider='google-oauth2').extra_data.get('access_token'):  # noqa
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        service = connect_helper(request.user)
        eventsResult = service.events().list(calendarId='primary').execute()
        events = eventsResult.get('items', [])
        for event in events:
            save_event(event, request.user)
        context['events'] = events
    # import pdb; pdb.set_trace()
    return render(request, 'index.html', context)


def login(request):
    return render(request, 'login.html', {})


def logout(request):
    auth_logout(request)
    return redirect(reverse('login'))


def connect_helper(user):
    social = user.social_auth.get(provider='google-oauth2')
    access_token = social.extra_data.get('access_token')
    credentials = AccessTokenCredentials(access_token, 'my-user-agent/1.0')
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build(serviceName='calendar', version='v3', http=http)
    return service


def save_event(event, user):
    if not event and user:
        return None
    try:
        # import pdb; pdb.set_trace()
        print('e:', event)
        event_data = Events(user=user, description=event.get('description'),
                            updated=datetime.strptime(event.get('updated'),
                                                      "%Y-%m-%dT%H:%M:%S.%fZ"))
        event_data.save()
        return event_data
    except IntegrityError as e:
        print(e.__cause__)
        return None
