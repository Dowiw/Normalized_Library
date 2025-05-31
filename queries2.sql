-- 1. Count of Books Per Author (Aggregation, GROUP BY, HAVING)
-- Find all authors who have written more than 3 books.
SELECT a.author_name, COUNT(b.book_id) AS book_count
FROM author a
JOIN book b ON a.author_id = b.author_id
GROUP BY a.author_name
HAVING COUNT(b.book_id) > 3;


-- 2. Find All Books Borrowed in a Date Range (Filtering with WHERE/BETWEEN)
-- List all books borrowed between January and March 2025, with their borrowers.
SELECT b.title, br.borrow_date, u.user_name
FROM borrow br
JOIN book b ON br.book_id = b.book_id
JOIN user u ON br.user_id = u.user_id
WHERE br.borrow_date BETWEEN '2025-01-01' AND '2025-03-31';


-- 3. Top 5 Most Borrowed Books (JOIN, Aggregation, ORDER BY)
-- Show the top 5 most borrowed books in the library.
SELECT b.title, COUNT(br.borrow_id) AS borrow_count
FROM book b
JOIN borrow br ON b.book_id = br.book_id
GROUP BY b.title
ORDER BY borrow_count DESC
LIMIT 5;


-- 4. Users Who Have Never Borrowed a Book (Subquery)
-- Find all users who have never borrowed a book.
SELECT u.user_name
FROM user u
WHERE u.user_id NOT IN (
    SELECT DISTINCT br.user_id FROM borrow br
);


-- 5. Average Borrow Duration Per User (CTE, Window Function)
-- For each user, show their average borrow duration (in days), sorted by highest average.
WITH borrow_durations AS (
  SELECT 
    br.user_id,
    DATEDIFF(br.return_date, br.borrow_date) AS duration
  FROM borrow br
  WHERE br.return_date IS NOT NULL
)
SELECT 
  u.user_name,
  AVG(bd.duration) AS avg_borrow_days
FROM user u
JOIN borrow_durations bd ON u.user_id = bd.user_id
GROUP BY u.user_name
ORDER BY avg_borrow_days DESC;
