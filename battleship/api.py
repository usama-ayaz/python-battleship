import http

import flask

app = flask.Flask(__name__)

@app.route('/battleship', methods=['POST'])
def create_battleship_game():
    return flask.jsonify({}), http.HTTPStatus.NOT_IMPLEMENTED


@app.route('/battleship', methods=['PUT'])
def shot():
    return flask.jsonify({}), http.HTTPStatus.NOT_IMPLEMENTED


@app.route('/battleship', methods=['DELETE'])
def delete_battleship_game():
    return flask.jsonify({}), http.HTTPStatus.NOT_IMPLEMENTED
