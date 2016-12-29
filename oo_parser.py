import csv
import os
from config import credentials
from sql_account import  SqlAccount

def header_as_expected(expected_header, actual_header):
    if expected_header == actual_header:
        return True

def main(file, table_exists):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        with SqlAccount(os.path.splitext(file)[0], **credentials) as db:
            headers = next(reader)
            if table_exists:
                header_as_expected(db.table_headers(), headers)
            else:
                db.execute_create_table(headers)
            db.execute_file(reader)

main('contacts.csv', table_exists = False)
