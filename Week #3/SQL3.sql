SELECT B.Title, COUNT(R.Reservation_ID) AS Reservation_Count
FROM Reservation R
JOIN Book B ON R.Book_ID = B.Book_ID
GROUP BY B.Title
HAVING COUNT(R.Reservation_ID) > 0;
