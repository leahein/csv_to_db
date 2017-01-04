#!flask/bin/python

from flask import Flask, jsonify, request
from config import credentials
from sql_account import SqlAccount
import csv

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


@app.route('/contacts', methods=['POST'])
def create():
    reader = csv.reader(request.files['file'])
    headers = next(reader)
    validate_or_create_by(headers)
    db.execute_file(reader)
    return ('Your Contacts have been added.', 200)

def validate_or_create_by(headers):
    table_exists = request.form['table_exists']
    if table_exists == 'True':
        header_as_expected(db.table_headers(), headers)
    else:
        db.execute_create_table(headers)


def header_as_expected(expected_header, actual_header):
    if expected_header == actual_header:
        return True


if __name__ == '__main__':
    app.run(debug=True)

