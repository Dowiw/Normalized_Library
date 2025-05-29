import csv
import psycopg2
from psycopg2 import sql

# Configuration
HOST = "localhost"
USER = "postgres"
PASSWORD = "somerandompassword"
PORT = "5432"
initial_db = "postgres" # Initial Database
new_db_name = "library" # Database to create

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

# Staff table
cursor.execute("""
CREATE TABLE staff (
    staff_id INT PRIMARY KEY,
    staff_name TEXT NOT NULL,
    shift_id INT REFERENCES shift(shift_id)
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
    staff_id INT REFERENCES staff(staff_id),
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
    staff_id INT REFERENCES staff(staff_id),
    loan_id INT REFERENCES loan(loan_id),
    return_date DATE,
    return_time TIME
)
""")

# FILL THE TABLES UP

# First filling up tables without foreign keys
# Shift table
cursor.execute("""
INSERT INTO shift (shift_id, shift_name, shift_start, shift_end)
    VALUES (1, 'Morning', '08:00:00', '12:00:00'),
    (2, 'Afternoon', '12:00:00', '16:00:00'),
    (3, 'Evening', '16:00:00', '20:00:00'),
    (4, 'Night', '18:00:00', '22:00:00')
""")

# ID Type table
cursor.execute("""
INSERT INTO id_type_code (id_type_code, id_type_name)
    VALUES (1, 'Driver''s License'),
    (2, 'Passport'),
    (3, 'Residence Permit')
    (4, 'Student ID'),
    (5, 'Employee ID'),
    (6, 'Voter ID'),
    (7, 'Work Permit'),
    (8, 'Military ID')
""")

with open('staff.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        cursor.execute(
            """INSERT INTO staff (staff_id, staff_name, shift_id)
            VALUES (%s, %s, %s)
            ON CONFLICT (staff_id) DO UPDATE
            SET staff_name = EXCLUDED.staff_name,
            shift_id = EXCLUDED.shift_id;""",
            row
        )

with open('publisher.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        cursor.execute(
            """INSERT INTO publisher (publisher_id, publisher_name)
            VALUES (%s, %s)
            ON CONFLICT (publisher_id) DO UPDATE
            SET publisher_name = EXCLUDED.publisher_name;""",
            row
        )
