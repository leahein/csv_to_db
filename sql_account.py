'''
MySQL Convenience Class
'''

import pymysql

class SqlAccount(object):

    def __init__(self, table, **kwargs):
        '''Maintains the internal state of a database connection
        :param host: STR with name of host to connect to
        :param user: STR with user to authenticate as
        :param db: STR with name of database to connect to
        :param password: STR with password to authenticate user
        '''
        self.connection = pymysql.connect(**kwargs)
        self.cursor = self.connection.cursor()
        self.table = table

##########################
# SQL Query strings
##########################
    def select_all(self):
        return '''SELECT * FROM {};'''.format(self.table)

    def select_one(self):
        return '''SELECT * FROM {} WHERE id = %s'''.format(self.table)


    def insert_rows(self):
        return  """INSERT INTO {} VALUES (NULL, %s, %s, %s, %s, %s)""".format(self.table)

    def create_table(self):
        return """DROP TABLE IF EXISTS {table};
        CREATE TABLE {table} (
        id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        %s  CHAR(20),
        %s  CHAR(20),
        %s INT,
        %s CHAR(12),
        %s VARCHAR(320) )""".format(table=self.table)

    def select_column_names(self):
        return """SELECT column_name FROM information_schema.columns
        WHERE table_name = %s"""

#############################
# Execution of query strings
#############################

    def table_headers(self):
        '''Queries database for the column names
        * Get query for column names
        * Execute query and return it as tuple of tuples
        * Parse response to array of strings, excluding id, and return it
        '''
        query = self.select_column_names()
        headers = self.execute_query(query, self.table, fetch=True)
        return [col[0] for col in headers if col[0] != 'id']

    def execute_create_table(self, headers):
        '''Creates a database table with given headers from file
        :param headers: array of strings with headers from csv file
        '''
        query = self.create_table() % tuple(headers)
        self.execute_query(query)

    def execute_query(self, query, values='', fetch=False):
        '''Execute string sql query and commit to database
        If fetch = True, return tuple of tuples of the query result
        '''
        if values:
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)
        self.connection.commit()
        if fetch:
            return self.cursor.fetchall()

    def execute_file(self, file):
        '''Execute file by persisting to db line by line
        :param file: Open file
        '''
        query = self.insert_rows()
        [self.execute_query(query, tuple(row)) for row in file]

    def close(self):
        '''Close database connection'''
        self.connection.close()


    # def __enter__(self):
        # return self


    # def __exit__(self, type, value, traceback):
        # self.close()
