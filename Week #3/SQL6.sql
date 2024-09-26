SELECT U.Name, 'Librarian' AS Role
FROM User U
JOIN Librarian L ON U.User_ID = L.User_ID

UNION

SELECT U.Name, 'Regular User' AS Role
FROM User U
JOIN Regular_User RU ON U.User_ID = RU.User_ID;
