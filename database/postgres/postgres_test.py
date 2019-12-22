import unittest

import psycopg2

from postgres import Postgres

class Test(unittest.TestCase):
    postgres = Postgres(
        connstring='postgresql://test_user:test@localhost:5432/test_user'
    )

    def test_parse(self):
        connstring = 'postgresql://test_user:test@localhost:5432/test_user'
        user, pwd, host, port, db = self.postgres._parse(connstring)
        self.assertEqual(user, 'test_user')
        self.assertEqual(pwd, 'test')
        self.assertEqual(host, 'localhost')
        self.assertEqual(port, 5432)
        self.assertEqual(db, 'test_user')
    
    def test_connect(self):
        conn = self.postgres.get_connection()
        self.assertIsInstance(conn, psycopg2.extensions.connection)

    def test_query(self):
        query = """
        SELECT * FROM advertising 
        WHERE id=1
        LIMIT 1
        """
        rows = self.postgres.execute_query(query)
        row_id = rows[0]['id']
        self.assertIsInstance(rows, list)
        self.assertIsInstance(rows[0], psycopg2.extras.DictRow)
        self.assertEqual(row_id, 1)
    
    def test_disconnect(self):
        pass

if __name__ == "__main__":
    unittest.main()