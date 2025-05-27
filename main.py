import psycopg2
from psycopg2 import sql

# Database credentials
HOST = "localhost"
USER = "postgres"
PASSWORD = "somerandompassword"
PORT = "5432"

# Database to connect to at first
initial_db = "mydb"

# Name of database to create
new_db_name = "library"

# Connect to initial database first ('posgres')
connection = psycopg2.connect(
    dbname = initial_db,
    user = USER,
    password = PASSWORD,
    host = HOST,
    port = PORT
)

# Enable for database creations without transactions
connection.autocommit = True


# Cursor
