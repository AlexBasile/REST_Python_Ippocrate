__author__ = 'Alex'

import os
import httplib2
import json

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

        global calendars
        json_data = open(os.path.join(os.path.dirname(__file__), 'calendari.json'))
        calendars = json.load(json_data)
        json_data.close()

        """
        page_token = None
        while True:
            events = service_calendar.events().list(calendarId='primary').execute()
            for event in events['items']:
                print event['summary']
                page_token = events.get('nextPageToken')
            if not page_token:
                break
        """

    def create_reservation(self, request):
        event = {
            'summary': request['prenotazione'],
            'location': request['ospedale'],
            'start': {
                'dateTime': request['start']
            },
            'end': {
                'dateTime': request['end']
            }
        }

        id_c = filter(lambda t: t['struttura'] == request['ospedale'], calendars)[0][request['sala']]
        #creo evento e ritorno l'ID per le successive modifiche
        event_c = service_calendar.events().insert(calendarId=id_c, body=event).execute()
        return event_c['id']

    def delete_reservation(self, request):
        id_c = filter(lambda t: t['struttura'] == request['ospedale'], calendars)[0][request['sala']]
        event_id = request['id_google']
        service_calendar.events().delete(calendarId=id_c, eventId=event_id).execute()



    def modify_reservation(self):
        return 0

    def check_slot(self):
        return 0

    def free_slot(self, request):
        id_c = filter(lambda t: t['struttura'] == request['ospedale'], calendars)[0][request['sala']]

        freebusy_query = {
            "timeMin" : request['time_min'],
            "timeMax" : request['time_max'],
            "items" :[
              {
                "id" : id_c
              }
            ]
        }

        response = service_calendar.freebusy().query(body=freebusy_query)
        return response

    def create_calendars(self, request):

        print "inizio cancellazione"

        page_token = None
        while True:
            #Cancello tutti i calendari di tutte le strttureMediche/Sale/Medici
            calendar_list = service_calendar.calendarList().list(pageToken=page_token).execute()

            print calendar_list

            for calendar_list_entry in calendar_list['items']:
                service_calendar.calendarList().delete(calendarId=calendar_list_entry['id']).execute()

            print "page_token"
            page_token = calendar_list.get('nextPageToken')
            print "while"

            if not page_token:
                break

        print "finisco la cancellazione"

        #Elimino il vecchio calendari.json
        os.remove(os.path.join(os.path.dirname(__file__), 'calendari.json'))

        calendari = '{ "calendari" = ['

        structures = request['strutture']
        #per ciascuna struttura
        for struct in structures:

            calendari += '{ "struttura": "' + struct['nome'] + '",'
            calendari += '"entita_prenotabili" : [{'

            for medico in struct['medici']:
                calendar = {
                    'summary' : 'calendario medico ' + medico,
                    'timeZone' : 'Europe/Rome'
                }
                calendar_id = service_calendar.calendars().insert(body=calendar).execute()
                calendari += '"' + medico + '": "' + calendar_id + '",'

            for sala in struct['sale']:
                calendar = {
                    'summary' : 'calendario sala ' + sala,
                    'timeZone' : 'Europe/Rome'
                }
                calendar_id = service_calendar.calendars().insert(body=calendar).execute()
                calendari += '"' + sala + '": "' + calendar_id + '",'

            #tolgo la virgola all'ultimo elemento delle entita' prenotabile
            calendari = calendari[:-1]
            calendari += '},'

        calendari = calendari[:-1]
        calendari += "]}"
        print calendari

        with open('calendari.json.', 'w') as outfile:
            json.dump(calendari, outfile)
