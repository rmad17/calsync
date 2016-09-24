import httplib2
from datetime import datetime
from django.shortcuts import render, reverse, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from apiclient.discovery import build
from oauth2client.client import AccessTokenCredentials

from .models import Events
# Create your views here.


@login_required
def home(request):
    context = {}
    if request.user.social_auth.get(provider='google-oauth2').extra_data.get('access_token'):  # noqa
        service = connect_helper(request.user)
        eventsResult = service.events().list(calendarId='primary').execute()
        events = eventsResult.get('items', [])
        for event in events:
            update_or_create_event(event, request.user)
        context['events'] = events
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


def update_or_create_event(event, user):
    if not event and user:
        return None
    obj, event_data = Events.objects \
                        .update_or_create(user=user, description=event.get('description'),  # noqa
                                          updated=datetime.strptime(event.get('updated'), "%Y-%m-%dT%H:%M:%S.%fZ"),  # noqa
                                          google_id=event.get('id'))
    return event_data
