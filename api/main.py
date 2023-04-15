from flask import Flask, jsonify, make_response, request
from flask_restful import Api

from PostgresStorage import PostgresStorage

storage_session = PostgresStorage()
app = Flask(__name__)
app.config['SERVER_NAME'] = '0.0.0.0:5000'
api = Api(app)


@app.route('/users', methods=['GET'])
def get_users():
    page: int = 1
    try:
        page = int(request.args.get('page', default=1))
    except ValueError:
        pass
    return make_response(jsonify(storage_session.list_users(page=page - 1)))


if __name__ == '__main__':
    app.run(debug=True)
