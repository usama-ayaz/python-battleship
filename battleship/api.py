import http

import flask
from battleboard.models import BattlShipBoard

app = flask.Flask(__name__)
app.config['BOARD_DIMENSION'] = (10, 10)
# a global board state that keeps board status through out current thread of flask app
global_board = None

@app.route('/battleship', methods=['POST'])
def create_battleship_game():

    global global_board
    try:
        ships = flask.request.get_json().get("ships")
        global_board = BattlShipBoard(app.config.get('BOARD_DIMENSION'), ships)
        return flask.jsonify({}), http.HTTPStatus.OK 
    except Exception as e:
        return flask.jsonify({}), http.HTTPStatus.BAD_REQUEST    


@app.route('/battleship', methods=['PUT'])
def shot():
    global global_board
    try:
        if global_board:
            data = flask.request.get_json()
            status = global_board.hitShip( (data.get('x'), data.get('y')) )
            return flask.jsonify({"result": status}), http.HTTPStatus.OK

        else:
            raise "Exception Raised: Game Not Created"    
    except Exception as e:
        return flask.jsonify({}), http.HTTPStatus.BAD_REQUEST



@app.route('/battleship', methods=['DELETE'])
def delete_battleship_game():
    global global_board
    try:
        if global_board:
            global_board = None
            return flask.jsonify({}), http.HTTPStatus.OK
        else:
            raise "Exception Raised: Game Not Created"    
    except Exception as e:
        return flask.jsonify({}), http.HTTPStatus.BAD_REQUEST
    
