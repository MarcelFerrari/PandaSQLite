import unittest
import pandas as pd
from PandaSQLite import PandaSQLiteDB
import os

class TestPandaSQLiteDB(unittest.TestCase):
    def setUp(self):
        # Create a test database and connect to it
        self.db_path = "test.db"
        self.db = PandaSQLiteDB(self.db_path, verbose=False)

    def tearDown(self):
        # Close the connection and delete the test database
        self.db.con.close()
        os.remove(self.db_path)

    def test_query(self):
        # Test that query method returns a DataFrame
        df = self.db.query("SELECT * FROM sqlite_master")
        self.assertIsInstance(df, pd.DataFrame)

    def test_get_table(self):
        # Test that get_table method returns a DataFrame
        self.db.create_table("test_table", pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']}))
        df = self.db.get_table("test_table")
        self.assertIsInstance(df, pd.DataFrame)
        self.db.delete_table("test_table")

    def test_create_table(self):
        # Test that create_table method creates a table in the database
        df = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
        self.db.create_table("test_table", df)
        tables = self.db.show_tables()
        self.assertIn("test_table", tables.values)
        self.db.delete_table("test_table")

    # def test_update_table(self):
    #     # Test that update_table method updates the data in a table
    #     self.db.create_table("test_table", pd.DataFrame({'col1': [1.0, 2.0, 3.0], 'col2': ['a', 'b', 'c']}))
    #     df = pd.DataFrame({'col1': [2.0], 'col2': ['x']})
    #     self.db.update_table("test_table", df)
    #     updated_df = self.db.get_table("test_table")
    #     self.assertListEqual(updated_df.values.tolist(), [[2.0, 'x'], [2, 'b'], [3, 'c']])
    #     self.db.delete_table("test_table")

    def test_replace_table(self):
        # Test that replace_table method replaces the data in a table
        self.db.create_table("test_table", pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']}))
        df = pd.DataFrame({'col1': [4, 5, 6], 'col2': ['d', 'e', 'f']})
        self.db.replace_table("test_table", df)
        updated_df = self.db.get_table("test_table")
        self.assertListEqual(updated_df.values.tolist(), [[4, 'd'], [5, 'e'], [6, 'f']])
        self.db.delete_table("test_table")

    def test_append_to_table(self):
        # Test that append_to_table method appends data to a table
        self.db.create_table("test_table", pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']}))
        df = pd.DataFrame({'col1': [4, 5], 'col2': ['d', 'e']})
        self.db.append_to_table("test_table", df)
        updated_df = self.db.get_table("test_table")
        self.assertListEqual(updated_df.values.tolist(), [[1, 'a'], [2, 'b'], [3, 'c'], [4, 'd'], [5, 'e']])
        self.db.delete_table("test_table")

    def test_delete_table(self):
        # Test that delete_table method deletes a table from the
        self.db.execute("CREATE TABLE test_table (t INT)")
        self.db.delete_table("test_table")
        with self.assertRaises(Exception):
            self.db.get_table("test_table")

    def test_show_tables(self):
        # Test that query method returns a DataFrame
        df = self.db.show_tables()
        self.assertIsInstance(df, pd.DataFrame)

    def test_import_data(self):      
        file_names = {'csv': 'test.csv',
                  'excel': 'test.xlsx',
                  'json': 'test.json',
                  'parquet': 'test.parquet',
                  'feather': 'test.feather',
                  'pickle': 'test.pickle',
                  'excel': 'test.xlsx'}
        
        # Import data
        for format in ["csv", "excel", "json", "parquet", "feather", "pickle"]:
            self.db.import_data("test_table", f"./data/{file_names[format]}", format=format)
            q = self.db.get_table("test_table")
            self.assertListEqual(q.values.tolist(), [[1, 'a', True], [2, 'b', False], [3, 'c', True]])
            self.db.delete_table("test_table")
        
    def test_import_db(self):
        db1 = PandaSQLiteDB("db1.sql")
        db2 = PandaSQLiteDB("db2.sql")

        db1.import_data("test_table_1", "./data/test.csv", if_exists="replace")
        db2.import_data("test_table_2", "./data/test.csv", if_exists="replace")

        # Raise error
        with self.assertRaises(Exception):
            db1.import_db(db1)

        with self.assertRaises(Exception):
            db1.import_db("db1.sql")

        with self.assertRaises(Exception):
            db1.import_db(10)
            
        # Correct
        db1.import_db(db2)
        self.assertTrue(db1.get_table("test_table_1").equals(db2.get_table("test_table_2")))

        # Error
        db2.import_data("test_table_1", "./data/test.csv", if_exists="replace")
        
        with self.assertRaises(Exception):
            db1.import_db(db2)

        os.remove("db1.sql")
        os.remove("db2.sql")
        

if __name__ == "__main__":
    unittest.main()