import pandas as pd
import sqlite3 as sql

class PandasDB():
    # --- Class constructor ---- #
    def __init__(self, db_path: str, auto_commit: bool = True, verbose: bool = False):
        self.con = sql.connect(db_path)
        self.cur = self.con.cursor()
        self.auto_commit = auto_commit
        self.verbose = verbose
    
    # --- Useful decorators --- #

    def log_query(func):
        def wrapper(self, *args, **kwargs):
            if self.verbose:
                print(f"Executed: {args[0]}") 
            return func(self, *args, **kwargs)
        return wrapper

    def commit_on_complete(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            # Auto-commit changes
            if self.auto_commit:
                self.commit()
            return result
        return wrapper

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
        df.to_sql(tname, self.con, if_exists, index=False)

    # Update table
    @commit_on_complete
    def update_table(self, tname: str, df: pd.DataFrame) -> None:
        self.replace_table(self.get_table(tname).update(df))

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
    def import_data(self, tname: str, fpath: str, format: str, if_exists='fail', **kwargs)-> None:
        if(format == "csv"):
            self.create_table(tname, pd.read_csv(fpath, **kwargs), if_exists)
        elif(format == "fwf"):
            self.create_table(tname, pd.read_fwf(fpath, **kwargs), if_exists)
        elif(format =="excel"):
            self.create_table(tname, pd.read_excel(fpath, **kwargs), if_exists)
        elif(format == "json"):
            self.create_table(tname, pd.read_json(fpath, **kwargs), if_exists)
        else:
            frmts = ["csv", "fwf", "excel", "json"]
            print(("Unsupported format.\n"
                   "The supported formats are:\n"
                   f"{frmts}"))

    # --- Class destructor --- #
    def __del__(self):
        if self.auto_commit:
            self.commit()
        self.con.close()
