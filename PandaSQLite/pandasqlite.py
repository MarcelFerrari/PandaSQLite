# --- System imports ---
import pandas as pd
import sqlite3 as sql
import os

# --- PandaSQLite imports ---
from .errors import *
from .io import extension_to_format
from .decorator import *

class PandaSQLiteDB():
    # --- Class constructor ---- #
    def __init__(self, db_path: str, auto_commit: bool = True, verbose: bool = False):
        self.db_path = os.path.realpath(db_path)
        self.con = sql.connect(db_path)
        self.cur = self.con.cursor()
        self.auto_commit = auto_commit
        self.verbose = verbose

    # --- Table operations --- #
    # Execute query and return df
    @log_query
    def query(self, query: str) -> pd.DataFrame:
        return pd.read_sql_query(query, self.con)
    
    # Query full table
    def get_table(self, tname: str) -> pd.DataFrame:
        # Broken: return pd.read_sql_table(tname, self.con)
        return self.query(f"SELECT * FROM \"{tname}\"")
    
    # Create table from df
    @commit_on_complete
    def create_table(self, tname: str, df: pd.DataFrame, if_exists='fail') -> None:
        df.to_sql(tname, self.con, if_exists=if_exists, index=False)

    # # Update table
    # @commit_on_complete
    # def update_table(self, tname: str, df: pd.DataFrame) -> None:
    #     tmp = self.get_table(tname)
    #     tmp.update(df)
    #     self.replace_table(tname, tmp)

    # Update table from df
    @commit_on_complete
    def replace_table(self, tname: str, df: pd.DataFrame) -> None:
        df.to_sql(tname, self.con, if_exists='replace', index=False)

    # Append data from df to table
    @commit_on_complete
    def append_to_table(self, tname: str, df: pd.DataFrame) -> None:
        df.to_sql(tname, self.con, if_exists='append', index=False)

    # Delete table
    @commit_on_complete
    def delete_table(self, tname: str) -> None:
        self.cur.execute(f"DROP TABLE IF EXISTS \"{tname}\"")
        if self.verbose:
            print(f"Deleted table {tname}")

    # Execute SQL query with no output 
    @log_query   
    @commit_on_complete
    def execute(self, query: str) -> None:
        self.cur.execute(query) 

    def show_tables(self):
        return self.query("SELECT name from sqlite_master WHERE type='table'")

    # --- DB operations --- #
    def commit(self):
        self.con.commit()

    @commit_on_complete
    def import_data(self, tname: str, fpath: str, format: str = None, if_exists = 'fail', **kwargs) -> None:
        _, file_extension = os.path.splitext(fpath)
        
        if not format:
            try:
                format = extension_to_format[file_extension]
            except:
                raise UnableToDetermineImportFormat(file_extension)

        if format in ["csv", "fwf", "excel", "json", "parquet", "feather", "pickle"]:
            read_func = getattr(pd, f"read_{format}")
            self.create_table(tname, read_func(fpath, **kwargs), if_exists)
        else:
            raise UnsupportedImportFormat(format)

    @commit_on_complete
    def import_db(self, other, if_exists = 'fail', **kwargs) -> None:        
        
        if type(other) == PandaSQLiteDB:
            if self.db_path == other.db_path:
                raise AliasedDBMergeOperation
            
        elif type(other) == str:
            other = PandaSQLiteDB(other, auto_commit=False)

            if self.db_path == os.path.realpath(other):
                raise AliasedDBMergeOperation
        else:
            raise TypeError(f"Expecting str or PandaSQLiteDB, got {type(other)}")

        tables = other.show_tables()

        if if_exists == "fail":
            for i in self.show_tables()["name"]:
                for j in tables["name"]:
                    if i == j:
                        raise ConflictingTableName(i, self.db_path)

        for tname in tables["name"]:
            self.create_table(tname, other.get_table(tname), if_exists=if_exists)

    # --- Class destructor --- #
    def __del__(self):
        self.con.close()
