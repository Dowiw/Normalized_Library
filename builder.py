import psycopg2
from psycopg2 import sql

# Database credentials
HOST = "localhost"
USER = "postgres"
PASSWORD = "somerandompassword"
PORT = "5432"

# Database to connect to at first
initial_db = "postgres"

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

# Cursor for execution and query inputs
cursor = connection.cursor()

# First sql module to create database
cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(new_db_name)))
print(f"Database '{new_db_name}' created successfully.")

# Initially connect to new db using root
new_connection = psycopg2.connect(
    dbname = new_db_name,
    user = USER,
    password = PASSWORD,
    host = HOST,
    port = PORT
)
new_connection.autocommit = True
cursor = new_connection.cursor()

# Query all records
# cursor.execute("SELECT * FROM staff")
# cursor.execute("SELECT COUNT(*) FROM staff")
# print(cursor.fetchall())


# CREATE ALL TABLES
# ID Type table
cursor.execute("""
CREATE TABLE id_type_code (
    id_type_code INT PRIMARY KEY,
    id_type_name TEXT NOT NULL
)
""")

# Shift table
cursor.execute("""
CREATE TABLE shift (
    shift_id INT PRIMARY KEY,
    shift_name TEXT NOT NULL,
    shift_start TIME NOT NULL,
    shift_end TIME NOT NULL               
)
""")

# Publisher table
cursor.execute("""
CREATE TABLE publisher (
    publisher_id INT PRIMARY KEY,
    publisher_name TEXT NOT NULL
)
""")

# Author table
cursor.execute("""
CREATE TABLE author (
    author_id INT PRIMARY KEY,
    author_name TEXT NOT NULL
)
""")

# User table
cursor.execute("""
CREATE TABLE "user" (
    user_id INT PRIMARY KEY,
    user_name TEXT NOT NULL,
    id_type INT REFERENCES id_type_code(id_type_code),
    phone_no TEXT,
    email TEXT
)
""")

# Book Table
cursor.execute("""
CREATE TABLE book (
    book_id INT PRIMARY KEY,
    book_title TEXT NOT NULL,
    author_id INT REFERENCES author(author_id),
    publisher_id INT REFERENCES publisher(publisher_id)
)
""")

# Copy table
cursor.execute("""
CREATE TABLE copy (
    copy_id INT PRIMARY KEY,
    book_id INT REFERENCES book(book_id),
    status TEXT NOT NULL
)
""")

# Loan table
cursor.execute("""
CREATE TABLE loan (
    loan_id INT PRIMARY KEY,
    user_id INT REFERENCES "user"(user_id),
    copy_id INT REFERENCES copy(copy_id),
    borrow_date DATE,
    borrow_time TIME,
    due_date DATE
)
""")

# Return table
cursor.execute("""
CREATE TABLE return (
    return_id INT PRIMARY KEY,
    loan_id INT REFERENCES loan(loan_id),
    return_date DATE,
    return_time TIME
)
""")

# Staff table
cursor.execute("""
CREATE TABLE staff (
    staff_id INT PRIMARY KEY,
    staff_name TEXT NOT NULL,
    shift_id INT REFERENCES shift(shift_id)
)
""")

