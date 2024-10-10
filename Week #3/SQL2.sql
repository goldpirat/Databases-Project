SELECT B.Title, U.Username
FROM Borrowing BR
JOIN Book B ON BR.Book_ID = B.Book_ID
JOIN User U ON BR.User_ID = U.User_ID
WHERE U.Role = 'Regular User';  -- Fetch only regular users
