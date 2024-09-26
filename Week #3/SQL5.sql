SELECT B.Title, U.Name
FROM Reservation R
JOIN Book B ON R.Book_ID = B.Book_ID
JOIN Librarian L ON R.User_ID = L.User_ID
JOIN User U ON L.User_ID = U.User_ID;
