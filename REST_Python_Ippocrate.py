from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from conn_calendar import Connector
from time import sleep


con = Connector()
app = Flask(__name__)


"""
calendari = [
    {
        'maria vittoria': {
            'radiologia': u'id calendario',
            'cardiologia': u'id calenda'
        }
    }

]
"""
"""
@app.route('/todo/api/v1.0/tasks', methods=['PUT'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201
"""


#contenuto del paramentro post: un json contente le informazioni dell'evento
@app.route('/ippocrate/calendar/v1.0/new_event/', methods=['POST'])
def create_reservation():

    if not request.json or not 'struttura' in request.json:
        abort(400)
    print("faccio la creazione")    #facile a dirsi
    print request.json
    id_google = con.create_reservation(request.json)
    response = {
        'code': '201',
        'id': id_google
    }
    return jsonify(response), 201

@app.route('/ippocrate/calendar/v1.0/delete_event/', methods=['POST'])
def delete_reservation():

    if not request.json or not 'struttura' in request.json:
        abort(400)
    print("faccio al cancellazione")
    con.delete_reservation(request.json)
    response = {
        'code': '201',
        'id': 'evento cancellato correttamente'
    }

    return jsonify(response), 201

@app.route('/ippocrate/calendar/v1.0/check_slot/', methods=['POST'])
def check_slot():

    if not request.json or not 'struttura' in request.json:
        abort(400)
    print("faccio il check")
    response = {
        'code': '201',
        'message': 'slot disponibile'
    }
    return jsonify(response), 201

@app.route('/ippocrate/calendar/v1.0/is_slot_free/', methods=['POST'])
def slots_free():

    if not request.json or not 'struttura' in request.json:
        abort(400)

    print(request.json)
    ris = con.free_slot(request.json)
    if ris:
        code = '201'
        messaggio = 'orario libero'
    else:
        code = '403'
        messaggio = 'slot selezionato occupato'
    response = {
        'code': code,
        'id': messaggio
    }
    return jsonify(response), 201

@app.route('/ippocrate/calendar/v1.0/get_calendar/', methods=['POST'])
def get_calendar():

    if not request.json or not 'struttura' in request.json:
        abort(400)
    id = con.get_calendar_id(request.json)
    response = {
        'code': '201',
        'id': id
    }
    return jsonify(response), 201

@app.errorhandler(404)
def not_found(error):
    print error
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(500)
def internal_server_error(error):
    print error
    return make_response(jsonify({'error': 'Internal Server Error'}), 500)

if __name__ == '__main__':
    app.run()
