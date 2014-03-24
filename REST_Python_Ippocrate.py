from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from conn_calendar import Connector

con = Connector()
app = Flask(__name__)

#contenuto del paramentro post: un json contente le informazioni dell'evento
@app.route('/ippocrate/calendar/v1.0/new_event/', methods=['POST'])
def create_reservation():

    if not request.json or not 'ospedale' in request.json:
        abort(400)
    print("faccio la creazione")    #facile a dirsi
    id_google = con.create_reservation(request.json)
    response = {
        'code': '201',
        'id': id_google
    }
    return jsonify(response), 201

@app.route('/ippocrate/calendar/v1.0/delete_event/', methods=['POST'])
def delete_reservation():

    if not request.json or not 'ospedale' in request.json:
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

    if not request.json or not 'ospedale' in request.json:
        abort(400)
    print("faccio il check")
    response = {
        'code': '201',
        'message': 'slot disponibile'
    }
    return jsonify(response), 201

@app.route('/ippocrate/calendar/v1.0/slots_free/', methods=['POST'])
def slots_free():

    if not request.json or not 'ospedale' in request.json:
        abort(400)

    print(request.json)
    response = {
        'code': '200',
        'slots': [
            {
                'start': "123",
                'end': "456"
            },
            {
                'start': "097",
                'end': "098"
            },
            {
                'start': "099",
                'end': "100"
            }
        ]
    }
    return jsonify(response), 201



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run()
