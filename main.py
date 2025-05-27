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
cursor = connection.cursor()

# First sql module to create database
cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(new_db_name)))
print(f"Database '{new_db_name}' created successfully.")

# Initially connect to new db using root
new_connection = psycopg2.connect("host = localhost dbname = library user = root password = root")
cursor = new_connection.cursor()

# Create staff table (id, first_name, last_name, shift)
cursor.execute("CREATE TABLE IF NOT EXISTS staff("
"staff_id INT PRIMARY KEY NOT NULL," \
"staff_first_name TEXT NOT NULL," \
"staff_last_name TEXT NOT NULL," \
"staff_shift TEXT NOT NULL")

# Query all records
cursor.execute("SELECT * FROM staff")
cursor.execute("SELECT COUNT(*) FROM staff")
print(cursor.fetchall())

cursor.execute("INSERT INTO staff (staff_id, staff_first_name, staff_last_name, staff_shift)" \
"VALUES (1, 'John', 'Doe', 'Morning')")