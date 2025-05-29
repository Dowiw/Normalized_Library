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

# Connect to initial database first ('postgres')
print("Connecting to initial database...")
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
print(f"Creating new database '{new_db_name}'")
cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(new_db_name)))
print(f"Database '{new_db_name}' created successfully.")

# Initially connect to new db using root
print("Connecting to new database...")
new_connection = psycopg2.connect(
    dbname = new_db_name,
    user = USER,
    password = PASSWORD,
    host = HOST,
    port = PORT
)
new_connection.autocommit = True
cursor = new_connection.cursor()
print("Connected!")

# CREATE ALL TABLES
print("Creating tables... :")

# ID Type table
print("Creating id_type_code table... ")
cursor.execute("""
CREATE TABLE id_type_code (
    id_type_code INT PRIMARY KEY,
    id_type_name TEXT NOT NULL
)
""")

# Shift table
print("Creating shift table... ")
cursor.execute("""
CREATE TABLE shift (
    shift_id INT PRIMARY KEY,
    shift_name TEXT NOT NULL,
    shift_start TIME NOT NULL,
    shift_end TIME NOT NULL
)
""")

# Publisher table
print("Creating publisher table... ")
cursor.execute("""
CREATE TABLE publisher (
    publisher_id INT PRIMARY KEY,
    publisher_name TEXT NOT NULL
)
""")

# Author table
print("Creating author table... ")
cursor.execute("""
CREATE TABLE author (
    author_id INT PRIMARY KEY,
    author_name TEXT NOT NULL
)
""")

# User table
print("Creating user table... ")
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
print("Creating book table... ")
cursor.execute("""
CREATE TABLE book (
    book_id INT PRIMARY KEY,
    book_title TEXT NOT NULL,
    author_id INT REFERENCES author(author_id),
    publisher_id INT REFERENCES publisher(publisher_id)
)
""")

# Staff table
print("Creating staff table... ")
cursor.execute("""
CREATE TABLE staff (
    staff_id INT PRIMARY KEY,
    staff_name TEXT NOT NULL,
    shift_id INT REFERENCES shift(shift_id)
)
""")

# Copy table
print("Creating copy table... ")
cursor.execute("""
CREATE TABLE copy (
    copy_id INT PRIMARY KEY,
    book_id INT REFERENCES book(book_id),
    status TEXT NOT NULL
)
""")

# Loan table
print("Creating loan table... ")
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
print("Creating return table... ")
cursor.execute("""
CREATE TABLE return (
    return_id INT PRIMARY KEY,
    staff_id INT REFERENCES staff(staff_id),
    loan_id INT REFERENCES loan(loan_id),
    return_date DATE,
    return_time TIME
)
""")
print("Done creating tables!")

# FILL THE TABLES UP
print("Filling tables up with relevant data from csv files... ")

# First filling up tables without foreign keys
print("Filling tables with no foreign keys...")

# Shift table
print("Filling shift table (independent)...")
cursor.execute("""
INSERT INTO shift (shift_id, shift_name, shift_start, shift_end)
    VALUES (1, 'Morning', '08:00:00', '12:00:00'),
    (2, 'Afternoon', '12:00:00', '16:00:00'),
    (3, 'Evening', '16:00:00', '20:00:00'),
    (4, 'Night', '18:00:00', '22:00:00')
""")

# ID Type table
print("Filling id_type_code table (independent)...")
cursor.execute("""
INSERT INTO id_type_code (id_type_code, id_type_name)
    VALUES (1, 'Driver''s License'),
    (2, 'Passport'),
    (3, 'Residence Permit'),
    (4, 'Student ID'),
    (5, 'Employee ID'),
    (6, 'Voter ID'),
    (7, 'Work Permit'),
    (8, 'Military ID')
""")

print("Filling tables with foreign keys...")
print("Filling staff table...")
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

print("Filling publisher table...")
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

print("Filling author table...")
with open('author.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        cursor.execute(
            """INSERT INTO author (author_id, author_name)
            VALUES (%s, %s)
            ON CONFLICT (author_id) DO UPDATE
            SET author_name = EXCLUDED.author_name;""",
            row
        )

print("Filling book table...")
with open('book.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        cursor.execute(
            """INSERT INTO book (book_id, book_title, author_id, publisher_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (book_id) DO UPDATE
            SET book_title = EXCLUDED.book_title,
            author_id = EXCLUDED.author_id,
            publisher_id = EXCLUDED.publisher_id;""",
            row
        )

print("Filling user table...")
with open('user.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        cursor.execute(
            """INSERT INTO "user" (user_id, user_name, id_type, phone_no, email)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (user_id) DO UPDATE
            SET user_name = EXCLUDED.user_name,
            id_type = EXCLUDED.id_type,
            phone_no = EXCLUDED.phone_no,
            email = EXCLUDED.email;""",
            row
        )

print("Filling copy table...")
with open('copy.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        cursor.execute(
            """INSERT INTO copy (copy_id, book_id, status)
            VALUES (%s, %s, %s)
            ON CONFLICT (copy_id) DO UPDATE
            SET book_id = EXCLUDED.book_id,
            status = EXCLUDED.status;""",
            row
        )

print("Filling loan table...")
with open('loan.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        cursor.execute(
            """INSERT INTO loan (loan_id, staff_id, user_id, copy_id, borrow_date, borrow_time, due_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (loan_id) DO UPDATE
            SET staff_id = EXCLUDED.staff_id,
            user_id = EXCLUDED.user_id,
            copy_id = EXCLUDED.copy_id,
            borrow_date = EXCLUDED.borrow_date,
            borrow_time = EXCLUDED.borrow_time,
            due_date = EXCLUDED.due_date;""",
            row
        )

print("Filling return table...")
with open('return.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        cursor.execute(
            """INSERT INTO return (return_id, staff_id, loan_id, return_date, return_time)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (return_id) DO UPDATE
            SET staff_id = EXCLUDED.staff_id,
            loan_id = EXCLUDED.loan_id,
            return_date = EXCLUDED.return_date,
            return_time = EXCLUDED.return_time;""",
            row
        )

print("Done filling tables!")
print("Builder script done! Use the library database for queries!")