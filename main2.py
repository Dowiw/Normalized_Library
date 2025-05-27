import psycopg2
from psycopg2 import sql

# Database credentials
HOST = "localhost"
USER = "postgres"
PASSWORD = "somerandompassword"
PORT = "5432"
INITIAL_DB = "mydb"
NEW_DB_NAME = "library"

# Step 1: Connect to initial database to create the new one
conn = psycopg2.connect(
    dbname=INITIAL_DB,
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT
)
conn.autocommit = True
cur = conn.cursor()
cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(NEW_DB_NAME)))
print(f"Database '{NEW_DB_NAME}' created successfully.")
conn.close()

# Step 2: Connect to the newly created 'library' database
conn = psycopg2.connect(
    dbname=NEW_DB_NAME,
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT
)
cur = conn.cursor()

# Step 3: Create all tables

cur.execute("""
CREATE TABLE id_type_code (
    id_type_code INT PRIMARY KEY,
    id_type_name TEXT NOT NULL
)
""")

cur.execute("""
CREATE TABLE publisher (
    publisher_id INT PRIMARY KEY,
    publisher_name TEXT NOT NULL
)
""")

cur.execute("""
CREATE TABLE author (
    author_id INT PRIMARY KEY,
    author_name TEXT NOT NULL
)
""")

cur.execute("""
CREATE TABLE "user" (
    user_id INT PRIMARY KEY,
    user_name TEXT NOT NULL,
    id_type INT REFERENCES id_type_code(id_type_code),
    phone_no TEXT,
    email TEXT
)
""")

cur.execute("""
CREATE TABLE book (
    book_id INT PRIMARY KEY,
    book_title TEXT NOT NULL,
    author_id INT REFERENCES author(author_id),
    publisher_id INT REFERENCES publisher(publisher_id)
)
""")

cur.execute("""
CREATE TABLE copy (
    copy_id INT PRIMARY KEY,
    book_id INT REFERENCES book(book_id),
    status TEXT NOT NULL
)
""")

cur.execute("""
CREATE TABLE loan (
    loan_id INT PRIMARY KEY,
    user_id INT REFERENCES "user"(user_id),
    copy_id INT REFERENCES copy(copy_id),
    borrow_date DATE,
    borrow_time TIME,
    due_date DATE
)
""")

cur.execute("""
CREATE TABLE return (
    return_id INT PRIMARY KEY,
    loan_id INT REFERENCES loan(loan_id),
    return_date DATE,
    return_time TIME
)
""")

cur.execute("""
CREATE TABLE staff (
    staff_id INT PRIMARY KEY,
    staff_name TEXT NOT NULL,
    shift TEXT NOT NULL
)
""")

# Step 4: Insert all records

cur.execute("""
INSERT INTO id_type_code VALUES
(1, 'Passport'),
(2, 'Driver''s License'),
(3, 'Resident''s Permit')
""")

cur.execute("""
INSERT INTO publisher VALUES
(1, 'Program Press'),
(2, 'Ovals'),
(3, 'Tech Press')
""")

cur.execute("""
INSERT INTO author VALUES
(1, 'Donald Trump'),
(2, 'Monjardin KAB'),
(3, 'Lucy Chang')
""")

cur.execute("""
INSERT INTO "user" VALUES
(1, 'John Hannes', 1, '+49152242124', 'john@example.com'),
(2, 'Mary Jane', 2, '+49153367830', 'mary@example.com'),
(3, 'Tony Stark', 1, '+49154432107', 'richest@example.com')
""")

cur.execute("""
INSERT INTO book VALUES
(1, 'The Tariff', 1, 2),
(2, 'Database Designs', 3, 3),
(3, 'I love C-lang', 2, 1)
""")

cur.execute("""
INSERT INTO copy VALUES
(1, 1, 'Available'),
(2, 1, 'On Loan'),
(3, 2, 'Available')
""")

cur.execute("""
INSERT INTO loan VALUES
(1, 2, 3, '2025-04-01', '10:30', '2025-04-15'),
(2, 1, 1, '2025-03-25', '09:15', '2025-04-10'),
(3, 3, 2, '2024-04-02', '13:40', '2025-04-16')
""")

cur.execute("""
INSERT INTO return VALUES
(1, 2, '2025-04-10', '11:20'),
(2, 1, '2025-04-15', '14:45'),
(3, 3, '2025-04-16', '16:30')
""")

cur.execute("""
INSERT INTO staff VALUES
(1, 'John Doe', 'Morning'),
(2, 'Jane Doe', 'Evening'),
(3, 'Tom Brown', 'Night')
""")

# Step 5: Commit and close
conn.commit()
cur.close()
conn.close()

print("All tables created and populated successfully.")
