SELECT B.Title, U.Name
FROM Borrowing BR
JOIN Book B ON BR.Book_ID = B.Book_ID
JOIN Regular_User RU ON BR.User_ID = RU.User_ID
JOIN User U ON RU.User_ID = U.User_ID;
