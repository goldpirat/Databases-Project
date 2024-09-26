SELECT B.Title, AVG(RV.Rating) AS Average_Rating
FROM Review RV
JOIN Book B ON RV.Book_ID = B.Book_ID
GROUP BY B.Title;
