-- 1. Count of books per Author that authored three books and more, and their loan count by copy (COUNT, GROUP BY, HAVING)
SELECT a.author_name, COUNT(DISTINCT b.book_id) AS book_count, COUNT(l.loan_id) AS loan_count
FROM author a
JOIN book b ON a.author_id = b.author_id
JOIN "copy" c ON b.book_id = c.book_id
LEFT JOIN loan l ON c.copy_id = l.copy_id -- This LEFT JOIN for NULL books (no loans)
GROUP BY a.author_name
HAVING COUNT(DISTINCT b.book_id) > 3 -- Select only authors with books more than 3
ORDER BY book_count;


-- 2. Find All Books Loaned in a Range ordered by date (Filtering with WHERE/BETWEEN)
SELECT l.borrow_date, b.book_title, c.copy_id, u.user_name
FROM loan l
JOIN "copy" c ON l.copy_id = c.copy_id
JOIN book b ON c.book_id = b.book_id
JOIN "user" u ON l.user_id = u.user_id
WHERE l.borrow_date BETWEEN '2025-01-01' AND '2025-03-31' -- Ensure this is the time frame wanted
ORDER BY borrow_date;


-- 3. Top 5 Most Loaned Books (JOIN, COUNT, ORDER BY)
SELECT b.book_title, a.author_name, COUNT(l.copy_id) AS loan_count
FROM loan l
JOIN "copy" c ON l.copy_id = c.copy_id
JOIN book b ON c.book_id = b.book_id
JOIN author a ON b.author_id = a.author_id
GROUP BY b.book_title, a.author_name
ORDER BY loan_count DESC
-- Limit 5 can be modifiable to have an extensive ranking
LIMIT 5; 


-- 4. Users Who Have Never Borrowed a Book (Subquery)
SELECT u.user_name, u.user_id
FROM "user" u
WHERE u.user_id NOT IN (
    SELECT DISTINCT l.user_id FROM loan l
)


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
