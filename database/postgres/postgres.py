import json
import time
import logging
import re
from datetime import datetime

import psycopg2
import psycopg2.extras

logging.Formatter.converter = time.gmtime
logging.basicConfig(
    level=logging.DEBUG,
    filename=f'./postgres-log.log', 
    filemode='a', 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

class Postgres:
    def __init__(self, database=None, hostname=None, username=None, password=None, port=5432, connstring=None):
        logging.info('Connecting to postgres...')
        if connstring:
            username, password, hostname, port, database = self._parse(connstring)
        self.username = username
        self.password = password
        self.hostname = hostname
        self.database = database
        self.port = port or 5432
        self.connection_tries = 0
        self.conn = self.get_connection()
    
    def _parse(self, connstring=None):
        user, pwd, host, dbname, port = None, None, None, None, None
        pg_regex = re.compile('postgresql://(.*?):(.*?)@(.*?)/(.*)')
        host_regex = re.compile('(.*?):([0-9]+)')
        if pg_regex.match(connstring).groups():
            user, pwd, host, dbname = pg_regex.match(connstring).groups()
        if host_regex.match(host).groups():
            host, port = host_regex.match(host).groups()
            port = int(port)
        return user, pwd, host, port, dbname

    def get_connection(self):
        self.connection_tries += 1
        try:
            conn = psycopg2.connect(
                dbname=self.database,
                host=self.hostname,
                user=self.username,
                password=self.password
            )
            if conn:
                self.connection_tries = 0
                return conn
        except psycopg2.OperationalError:
            logging.warning('Error in getting Postgres connection')
            time.sleep(3)
            if self.connection_tries > 2:
                raise Exception('Error in getting Postgres connection')
            return self.get_connection()

    def close_connection(self):
        try:
            self.conn.close()
        except psycopg2.OperationalError:
            logging.warning('Error in closing Postgres connection')

    def execute_query(self, query='', values=()):
        try:
            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
        except (Exception, psycopg2.DatabaseError) as e:
            logging.warning('Error executing query: %s\nContext: %s' % (e, query))
            self.conn.rollback()
            if cursor:
                cursor.close()
            return []
        else:
            rows = cursor.fetchall()
            self.conn.commit()
            cursor.close()
        return rows if rows else []
