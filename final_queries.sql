--- 1. Count of Books Per Author (Aggregation, GROUP BY, HAVING)
SELECT a.author_name, COUNT(b.book_id) AS book_count
FROM author a
JOIN book b ON a.author_id = b.author_id
GROUP BY a.author_name
HAVING COUNT(b.book_id) > 3;


-- 2. Find All Books Loaned in a Range (Filtering with WHERE/BETWEEN)
SELECT
  l.borrow_date,
  b.book_title,
  c.copy_id,
  u.user_name
FROM loan l
JOIN "copy" c ON l.copy_id = c.copy_id
JOIN book b ON c.book_id = b.book_id
JOIN "user" u ON l.user_id = u.user_id
WHERE l.borrow_date BETWEEN '2025-01-01' AND '2025-03-31'
ORDER BY borrow_date;


-- 3. Top 5 Most Loaned Books (JOIN, Aggregation, ORDER BY)
SELECT b.book_title, COUNT(l.copy_id) AS loan_count
FROM loan l
JOIN "copy" c ON l.copy_id = c.copy_id
JOIN book b ON c.book_id = b.book_id
GROUP BY b.book_title
ORDER BY loan_count DESC
LIMIT 5;


-- 4. Users Who Have Never Borrowed a Book (Subquery)
SELECT u.user_name, u.user_id
FROM "user" u
WHERE u.user_id NOT IN (
    SELECT DISTINCT l.user_id FROM loan l
);


-- 5. Average Loan Duration Per User (CTE, Window Function) for bonus :- )
WITH loan_duration AS (
  SELECT 
    l.user_id,
    (r.return_date - l.borrow_date) AS duration
  FROM loan l
  JOIN "return" r ON l.loan_id = r.loan_id
  WHERE r.return_date IS NOT NULL
)
SELECT 
  u.user_name,
  ROUND(AVG(l.duration), 2) AS avg_loan_days
FROM "user" u
JOIN loan_duration l ON u.user_id = l.user_id
GROUP BY u.user_name
ORDER BY avg_loan_days DESC;
