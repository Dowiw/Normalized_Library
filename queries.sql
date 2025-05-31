--- 1. Finding the average borrow length of each books that are over 10 days
SELECT b.book_title, ROUND(AVG(r.return_date - l.borrow_date), 2) AS avg_days_borrowed
    FROM  loan l
JOIN 
    return r ON l.loan_id = r.loan_id
JOIN 
    book b ON b.book_id = b.book_id
GROUP BY book_title
HAVING AVG(r.return_date - l.borrow_date) > 10;

--- 2.  Finding how many times each books have been borrowed this year
SELECT 
    b.book_id,
    COUNT(*) AS borrow_count
FROM 
    loan l
JOIN 
    "copy" b ON b.book_id = b.book_id
WHERE 
    l.borrow_date BETWEEN '2025-01-01' AND '2025-12-31'
GROUP BY 
    b.book_title;

--- 3. Finding the 10 most active borrowers
SELECT 
    u.user_name,
    COUNT(*) AS total_borrowed
FROM 
    loan l
JOIN 
    "user" u ON l.user_id = u.user_id
GROUP BY 
    u.user_name
ORDER BY 
    total_borrowed DESC
LIMIT 10;

--- 4. Finding the average book borrowed per user
SELECT 
    ROUND(AVG(user_borrowed.total), 2) AS avg_books_borrowed
FROM (
    SELECT 
        u.user_id, COUNT(*) AS total
    FROM 
        "user" u
    JOIN 
        loan l ON u.user_id = l.user_id
    GROUP BY 
        u.user_id
) 
user_borrowed;

--- 5. Finding the number of times books have been borrowed each month
SELECT 
    DATE_TRUNC('month', borrow_date) AS month,
    COUNT(*) AS total_loans
FROM 
    loan
GROUP BY 
    month
ORDER BY 
    month;
