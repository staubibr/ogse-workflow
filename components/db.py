from uuid import uuid4

import psycopg2

from components.logger import Logger


class DB:
    @property
    def conn(self):
        return self._conn

    @conn.setter
    def conn(self, value):
        self._conn = value

    @property
    def schema(self):
        return self._schema

    @schema.setter
    def schema(self, value):
        self._schema = value

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, value):
        self._cursor = value

    def __init__(self):
        self.conn = None
        self.schema = None
        self.cursor = None

    def connect(self, service, password, database, host, port):
        Logger.info('Connecting to database...')
        self.conn = psycopg2.connect(user=service, password=password, database=database, host=host, port=port)
        self.schema = "ogse_" + str(uuid4()).replace("-", "")

        Logger.info('Creating database schema...')
        self.execute("CREATE SCHEMA {0}".format(self.schema))

    def execute(self, statement):
        self.cursor = self.conn.cursor()
        self.cursor.execute(statement)
        self.cursor.close()
        self.conn.commit()

    def select(self, statement):
        self.cursor = self.conn.cursor()
        self.cursor.execute(statement)

        rows = self.cursor.fetchall()

        self.cursor.close()
        self.conn.commit()

        return rows

    def close(self):
        Logger.info('Dropping database schema...')
        self.execute("DROP SCHEMA {0} CASCADE".format(self.schema))
        self.conn.close()

    def rollback(self):
        self.conn.rollback()
