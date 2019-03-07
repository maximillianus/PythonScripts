import sqlite3
import createdb
from data import PURCHASES

DBNAME = 'example.db'
TABLENAME = 'stocks'


def main():
    # Create connection
    conn, cur = createdb.create_conn(DBNAME)

    # Truncate table
    createdb.truncate_table(TABLENAME, cur, conn)

    # insert data
    createdb.insert_to_table(tablename=TABLENAME, 
                             data=PURCHASES, 
                             cur=cur, 
                             conn=conn)
    
    # Select Data
    res = createdb.retrieve_data(TABLENAME, cur, conn)
    print('Data Result:')
    print(res)

    # Close conn
    conn.close()

if __name__ == "__main__":
    main()