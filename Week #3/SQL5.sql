SELECT B.Title, U.Username
FROM Reservation R
JOIN Book B ON R.Book_ID = B.Book_ID
JOIN User U ON R.User_ID = U.User_ID
WHERE U.Role = 'Librarian';  -- Fetch only librarians' reservations
