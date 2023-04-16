import os

from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from flask_restful import Api

from PostgresStorage import PostgresStorage

storage_session = PostgresStorage()
app = Flask(__name__)
CORS(app)
api = Api(app)

PAGE_SIZE = os.environ.get('PAGE_SIZE', default=10)


@app.route('/api/users', methods=['GET'])
def get_users():
    page: int = 1
    try:
        page = int(request.args.get('page', default=1))
    except ValueError:
        pass
    users_response = storage_session.list_users(page=page, page_size=PAGE_SIZE)
    return make_response(jsonify(users_response))


@app.route('/api/users/search/<string:name>', methods=['GET'])
def search_users(name: str):
    page: int = 1
    try:
        page = int(request.args.get('page', default=1))
    except ValueError:
        pass
    users_response = storage_session.search_users(name_partial=name, page=page, page_size=PAGE_SIZE)
    return make_response(jsonify(users_response))


if __name__ == '__main__':
    app.run(debug=True)
