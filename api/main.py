import os

from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from flask_restful import Api

from PostgresStorage import PostgresStorage

storage_session = PostgresStorage()
app = Flask(__name__)
CORS(app)
api = Api(app)

PAGE_SIZE: int = int(os.environ.get('PAGE_SIZE', default=10))


@app.route('/api/users', methods=['GET'])
def get_users():
    page: int = 1
    try:
        page = int(request.args.get('page', default=1))
    except ValueError:
        pass
    return make_response(jsonify({
        'users': storage_session.list_users(page=page, page_size=PAGE_SIZE),
        'total': storage_session.fetch_all_users_count()
    }))


@app.route('/api/users/search/<string:name>', methods=['GET'])
def search_users(name: str):
    page: int = 1
    try:
        page = int(request.args.get('page', default=1))
    except ValueError:
        pass
    return make_response(jsonify({
        'users': storage_session.search_users(name_partial=name, page=page, page_size=PAGE_SIZE),
        'total': storage_session.fetch_filtered_users_count(name_partial=name)
    }))


if __name__ == '__main__':
    app.run(debug=True)
