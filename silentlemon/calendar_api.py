# Calendar API abstraction

import os
import time
from math import floor

import httplib2

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

API_KEY = "AIzaSyB3oxnOVb99bIcrbuttt1P28dFIzV6h9qk"
CALENDAR_ID = "g1qvenh8ijdnjfq1ofhpa6qd34@group.calendar.google.com"

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Silent Lemon'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


class Calendar:

    def __init__(self):
        pass

    def getTodayEvents(self):
        return [
            {
                "description": "Meeting",
                "start": floor(time.time()),
                "end": floor(time.time() + 60 * 60)
            }
        ]

    def get_upcoming_events(self, n=10):
        """Shows basic usage of the Google Calendar API.

        Creates a Google Calendar API service object and outputs a list of the next
        10 events on the user's calendar.
        """
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        #print('Getting the upcoming 10 events')
        eventsResult = service.events().list(
            calendarId=CALENDAR_ID, timeMin=now, maxResults=n, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        if not events:
            #print('No upcoming events found.')
            return []

        def event2simple(ev):

            if 'description' in ev:
                desc = ev['summary'] + ' ' + ev['description']
            else:
                desc = ev['summary']

            return {
              'description': desc,
              'start': ev['start'].get('dateTime'),
              'end': ev['end'].get('dateTime'),
            }

        #for event in events:
        #    start = event['start'].get('dateTime', event['start'].get('date'))
        #    print(start, event['summary'])

        return list(map(event2simple, events))
