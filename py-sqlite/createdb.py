import sqlite3

DBNAME = 'example.db'

def create_conn(dbname):
    try:
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        return conn, cur
    except sqlite3.Error as e:
        print('SQLite3 Error connecting to db: %s' % e)
        return False, False
    except Exception as e:
        print('Other Error connecting to db: %s' % e)
        return False, False

    

def create_table(tablename, cur, conn):
    query = """
    CREATE TABLE {table}
    (date text, transaction text, stockname text, qty real, price real)
    """
    try:
        cur.execute(query.format(tablename))
        conn.commit()
        print('Success creating table!')
    except sqlite3.Error as e:
        print('Error during create table: %s' % e)

def insert_to_table(tablename, data, cur, conn):
    """
    tablename: string
    data: list of tuples/rows
    """
    assert isinstance(tablename, str), "tablename is not string!"
    assert isinstance(data, list), "data is not list!"
    print(data)

    query = """
    INSERT INTO {table} VALUES (?, ?, ?, ?, ?)
    """
    try:
        cur.executemany(query.format(table=tablename), data)
        conn.commit()
        print('Success inserting batch data!')
    except sqlite3.Error as e:
        print('Error during insert: %s' % e)

def retrieve_data(tablename, cur, conn, query = ''):
    if query == '':
        query = """
        SELECT * FROM {table}
        """
    
    try:
        res = cur.execute(query.format(table=tablename))
        res = res.fetchall()
        conn.commit()
        return res
    except sqlite3.Error as e:
        print('Error retrieving data: %s' % e)


def truncate_table(tablename, cur, conn):
    query = """
    DELETE FROM {table}
    """
    try:
        print(query.format(table=tablename))
        cur.execute(query.format(table=tablename))
        conn.commit()
        print('Success truncating table!')
    except sqlite3.Error as e:
        print('Error during truncating table: %s' % e)

    