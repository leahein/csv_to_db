#!flask/bin/python

from flask import Flask
from flask import jsonify, request

from sql_account import SqlAccount

credentials = {
         'host':     'localhost',
         'user':     'root',
         'db':       'contacts',
         'password': 'L5e3a2h4'
        }


app = Flask(__name__)
db = SqlAccount('contacts', **credentials)

@app.route('/contacts', methods=['GET'])
def index():
    contacts = db.execute_query(db.select_all(), fetch=True)
    return jsonify({'contacts': contacts})

@app.route('/contacts/<int:contact_id>', methods=['GET'])
def show(contact_id):
    contact = db.execute_query(db.select_one(), contact_id, fetch=True)
    return jsonify({'contact': contact})



if __name__ == '__main__':
    app.run(debug=True)


