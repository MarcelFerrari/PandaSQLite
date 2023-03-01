class UnableToDetermineImportFormat(Exception):
    """
        Raised when import_data is unable to automatically determine the format of the file to import
    """
    def __init__(self, format):
        self.message = ("Unable to infer file format from file extension.\n"
                        f"Detected file extension: \"{format}\"")
        super().__init__(self.message)

class UnsupportedImportFormat(Exception):
    """
        Raised when the data format is not supported
    """
    def __init__(self, format):
        self.message = ("Unsupported file format.\n"
                        f"Unable to import file of format \"{format}\".")
        super().__init__(self.message)

class AliasedDBMergeOperation(Exception):
    """
        Raised when trying to import database into itself
    """
    def __init__(self):
        self.message = ("Aliased database import operation.\n"
                        "Cannot import database into itself.")
        super().__init__(self.message)

class ConflictingTableName(Exception):
    """
        Raised when trying to import database, but there is a table name conflict
    """
    def __init__(self, tname, fpath):
        self.message = ("Conflicting table name.\n"
                        f"Table \"{tname}\" already exists in database located at \"{fpath}\".")
        super().__init__(self.message)