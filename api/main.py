from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from flask_restful import Api

from PostgresStorage import PostgresStorage

storage_session = PostgresStorage()
app = Flask(__name__)
CORS(app)
api = Api(app)


@app.route('/api/users', methods=['GET'])
def get_users():
    page: int = 1
    try:
        page = int(request.args.get('page', default=1))
    except ValueError:
        pass
    return make_response(jsonify(storage_session.list_users(page=page - 1)))


if __name__ == '__main__':
    app.run(debug=True)
