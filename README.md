# PandaSQLite

PandaSQLite is a lightweight wrapper library that combines the power of SQLite databases with the ease of use of Python numerical libraries like pandas, numpy, scipy, etc. This library allows you to store and manage data using a modern SQLite database, while still being able to use query results seamlessly in python.

## Why bother with PandaSQLite?

### Features
- Fast and reliable data storage and management.
- Easy to use, with no setup required.
- Designed for use in Jupyter notebooks.
- Easily import data from different file formats.
- Leverage powerful SQL syntax for advanced data manipulation and analysis.

### Advantages
- Fast and reliable data storage and management.
- SQL is a declarative language, which optimizes your queries automatically in a way that imperative languages cannot. SQL will be almost certainly faster than Python scripts that parse data from disk!
- All data stored in a single binary file, keeping your data organized, tidy and much easier to share.
- Materialize intermediate results efficiently to speed up your data analysis.
- Speed up your code automatically using indices.

## Getting Started
### Requirements
PandaSQLite only supports Python 3 and is built on top of the `pandas` and `sqlite3` packages.

### Installation

To start using PandaSQLite, simply install the library using pip:

```
pip install PandaSQLite
```

Once the library is installed, you can start using it in your Python projects or Jupyter notebooks.

### Basic usage
This script defines the most basic usage of the library. The raw data must be imported in the database only once.
```py
from PandaSQLite import PandaSQLiteDB

# Create/open database
db = PandaSQLiteDB("my_database.sql")

# Import raw data -- must only be done once!
# Import example CSV data
db.import_data("my_table", "my_csv.csv", format="csv")

# Execute query with no return value
db.execute("INSERT INTO my_table VALUES (...)")

# Query dataframe with return values
df = db.query("SELECT * FROM my_table")
```

For a more comprehensive showcase of features, check out the examples in the examples directory to get started.

### Documentation
The documentation for PandaSQLite is [available here](https://github.com/MarcelFerrari/PandaSQLite/wiki)

### Common problems
`TypeError: 'NoneType' object is not iterable`:<br>
This issue is usually caused by executing a query with no return data in the `db.query()` function, which should only be used for queries that return a table ("SELECT" queries). Use the `db.execute()` function for queries with no return data (e.g: "INSERT", "UPDATE", "ALTER", ... queries).
<hr>