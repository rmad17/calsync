import httplib2
import json
from datetime import datetime
from django.shortcuts import render, reverse, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from apiclient.discovery import build
from oauth2client.client import AccessTokenCredentials

from .models import Events
# Create your views here.


@login_required
@csrf_exempt
def home(request):
    context = {}
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8')).get('data')
        service = connect_helper(request.user)
        eventsResult = service.events().list(calendarId='primary').execute()
        events = eventsResult.get('items', [])
        c = 0
        for event in events:
            event['summary'] = data[c]
            c = c + 1
            event = service.events().update(calendarId='primary', eventId=event.get('id'), body=event).execute()  # noqa
            update_or_create_event(event, request.user)
        context['events'] = events
        return render(request, 'index.html', context)
    if request.user.social_auth.get(provider='google-oauth2').extra_data.get('access_token'):  # noqa
        service = connect_helper(request.user)
        eventsResult = service.events().list(calendarId='primary').execute()
        events = eventsResult.get('items', [])
        for event in events:
            update_or_create_event(event, request.user)
        context['events'] = events
    return render(request, 'index.html', context)


@login_required
@csrf_exempt
def create_event(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8')).get('data')
        service = connect_helper(request.user)
        event = {
          'summary': 'Google I/O 2015',
          'location': '800 Howard St., San Francisco, CA 94103',
          'description': 'A chance to hear more about Google',
          'start': {
            'dateTime': '2015-05-28T09:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
          },
          'end': {
            'dateTime': '2015-05-28T17:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
          },
          'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=2'
          ],
          'attendees': [
            {'email': 'lpage@example.com'},
            {'email': 'sbrin@example.com'},
          ],
          'reminders': {
            'useDefault': False,
            'overrides': [
              {'method': 'email', 'minutes': 24 * 60},
              {'method': 'popup', 'minutes': 10},
            ],
          },
        }
        event['summary'] = data
        event = service.events().insert(calendarId='primary', body=event).execute()  # noqa
        update_or_create_event(event, request.user)
        return JsonResponse({'message': 'successful'}, status=200)


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
    try:
        obj, event_data = Events.objects \
                        .update_or_create(user=user, description=event.get('summary'),  # noqa
                                          updated=datetime.strptime(event.get('updated'), "%Y-%m-%dT%H:%M:%S.%fZ"),  # noqa
                                          google_id=event.get('id'))
    except IntegrityError as e:
        print('Error:', e.__cause__)
        return None
    return event_data
