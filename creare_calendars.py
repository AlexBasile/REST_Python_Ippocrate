import os
import httplib2
import json
from time import sleep

from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run
from oauth2client.file import Storage
from apiclient import discovery

"""
def create_calendar_google(nome):
    #accesso con autenticazione
    http = httplib2.Http()
    http = credentials.authorize(http)

    #creo un servizio per accedere al calendario dell'account
    service_calendar = discovery.build(serviceName='calendar', version='v3', http=http, developerKey='AIzaSyBNEvVjXujWST-rUrbMWqn_Ckh6qVuupUc')

    #creo un calendario
    calendar = {
        'summary': nome,
        'timeZone': 'Europe/Rome'
    }

    #eseguo l'operazione remota
    calendar_id = service_calendar.calendars().insert(body=calendar).execute()
    return calendar_id['id']

#json_data = open('calendari.json')
#calendars = json.load(json_data)
#json_data.close()

#richiesta
global strutture
strutture = [
    {
        u'sale': [u'Elettrocardiografia', u'Sala gessi', u'Analisi', u'Palestra per riabilitazione'],
        u'medici': [u'2202', u'7007'],
        u'nome': u'Maria Vittoria'
    }, {
        u'sale': [u'Radiografia', u'RMN', u'Sala gessi', u'Analisi', u'Palestra per riabilitazione'],
        u'medici': [u'house', u'1101', u'4004', u'9000', u'2002'],
        u'nome': u'CTO'
    }, {
        u'sale': [u'Elettrocardiografia', u'Radiografia', u'RMN', u'Palestra per riabilitazione'],
        u'medici': [u'6006', u'3000', u'5505', u'7000', u'5000'],
        u'nome': u'Amedeo di Savoia'
    }, {
        u'sale': [u'Elettrocardiografia', u'Radiografia', u'RMN', u'Sala gessi'],
        u'medici': [u'4404', u'1001', u'4000', u'9009', u'8008'],
        u'nome': u'Molinette'
    }, {
        u'sale': [u'Radiografia', u'RMN', u'Analisi', u'Palestra per riabilitazione', u'Elettrocardiografia'],
        u'medici': [u'2222', u'3333', u'8808', u'7777', u'6666', u'5555', u'1111'],
        u'nome': u'R.I.B.A.'
    }, {
        u'sale': [u'Radiografia', u'RMN', u'Analisi', u'Palestra per riabilitazione', u'Elettrocardiografia'],
        u'medici': [u'7707', u'9909'],
        u'nome': u'Corba'
    }, {
        u'sale': [u'RMN', u'Analisi', u'Palestra per riabilitazione', u'Elettrocardiografia'],
        u'medici': [u'hershel', u'4444'],
        u'nome': u'C.D.C'
    }
]

def create_all_calendar():

    calendari = '['
    for struttura in strutture:

        calendari += '{ "struttura": "' + struttura['nome'] + '",'
        print struttura['nome']

        medici = struttura['medici']
        for medico in medici:
            #salvo l'id del calendario appena creato nella json string
            try:
                id = create_calendar_google('medico ' + medico)
                sleep(1)                #faccio una richiesta al secondo
            except Exception:
                print "\n" + calendari + "\n"
                print "eccezione"
                sleep(1500)             #se google mi butta fuori aspetto 30minuti prima di riprovare a creare nuovi cal
                id = create_calendar_google('medico ' + medico)
            pass
            calendari += '"' + medico + '": "' + id + '",'


        sale = struttura['sale']
        for sala in sale:
            #salvo l'id del calendario appena creato nella json string
            try:
                id = create_calendar_google('sala ' + sala)
                sleep(1)                #faccio al massimo una richiesta al second
            except Exception:
                print "\n" + calendari + "\n"
                print "eccezione"
                sleep(1500)             #se google mi butta fuori aspetto 30minuti prima di riprovare a creare nuovi cal
                id = create_calendar_google('sala ' + sala)
            pass
            calendari += '"' + sala + '": "' + id + '",'


        calendari = calendari[:-1]
        calendari += '},'
        print calendari

    calendari = calendari[:-1]
    calendari += ']'

    #salvo la json string in un file
    n = json.dumps(calendari, indent=4)
    d = json.loads(n, encoding='utf8')

    print d

    obj = open('calendari_test.json', 'w')
    obj.write(d)
    obj.close()

def main():
    create_all_calendar()

if __name__ == '__main__':

    #Effettuo la connessione a Calendar
    flow = flow_from_clientsecrets(os.path.join(os.path.dirname(__file__), 'client_secret.json'), scope='https://www.googleapis.com/auth/calendar', redirect_uri='http://localhost:8080')

    storage = Storage('credenziali.dat')
    credentials = storage.get()

    if credentials is None or credentials.invalid == True: credentials = run(flow, storage)

    main()

"""