__author__ = 'Alex'

import os
import httplib2

from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run
from oauth2client.file import Storage
from apiclient import discovery


class Connector:
    def __init__(self):

        flow = flow_from_clientsecrets(os.path.join(os.path.dirname(__file__), 'client_secret.json'),
                                       scope='https://www.googleapis.com/auth/calendar',
                                       redirect_uri='http://localhost:8080')

        storage = Storage('credenziali.dat')
        credentials = storage.get()

        if credentials is None or credentials.invalid == True: credentials = run(flow, storage)

        http = httplib2.Http()
        http = credentials.authorize(http)

        #creo un servizio per accedere al calendario dell'account
        global service_calendar
        service_calendar = discovery.build(serviceName='calendar',
                                           version='v3',
                                           http=http,
                                           developerKey='AIzaSyBNEvVjXujWST-rUrbMWqn_Ckh6qVuupUc')

        page_token = None
        while True:
            events = service_calendar.events().list(calendarId='primary').execute()
            for event in events['items']:
                print event['summary']
                page_token = events.get('nextPageToken')
            if not page_token:
                break

