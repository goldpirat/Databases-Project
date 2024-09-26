-- Adding more users
INSERT INTO User (Name, Email) VALUES
('Flori Kusari', 'fkusari@constructor.university'),
('Rron Dermaku', 'rdermaku@constructor.university'),
('Hannah Paulus', 'hpaulus@constructor.university'),
('Edin Berisha', 'eberisha@constructor.university'),
('Camila Pina Pinto', 'cpinto@constructor.university'),
('Lis Fazliu', 'lfazliu@constructor.university');

-- Adding more regular users and librarians
INSERT INTO Librarian (User_ID) VALUES (1);     -- Flori is a librarian
INSERT INTO Regular_User (User_ID) VALUES (2);  -- Rron is a regular user
INSERT INTO Regular_User (User_ID) VALUES (3);  -- Hannah is a regular user
INSERT INTO Regular_User (User_ID) VALUES (4);  -- Edin is a Regular user
INSERT INTO Regular_User (User_ID) VALUES (5);  -- Camila is a Regular user
INSERT INTO Regular_User (User_ID) VALUES (6);  -- Lis is a Regular user

-- Adding more books
INSERT INTO Book (Title, Author, ISBN, Available_Copies) VALUES
('48 Laws of Power', 'Robert Greene', '9780140280197', 2),
('Little Red Riding Hood (Keepsake Stories)', 'N/A', '9781577681984', 15),
('Moby Dick (Wordsworth Classics)', 'Melville Herman', '9781853260087', 7),
('The Bro Code', 'Barney Stinson - Matt Kuhn', '9781439110003', 32),
('The Kite Runner', 'Khaled Hosseini', '9781594631931', 14),
('The Laws of Human Nature', 'Robert Greene', '9781781259191', 8),
('The Witness', 'Sandra Brown', '9781455538263', 7),
('The Old Man and The Sea', 'Ernest Hemingway', '9798329875195', 5),
('The 7 Habits of Highly Effective People: 30th Anniversary Edition', 'Stephen R. Covey', '781982137274', 4);

-- Adding borrowing records
INSERT INTO Borrowing (User_ID, Book_ID, Borrow_Date, Return_Date, Status) VALUES
(3, 2, '2024-09-20', '2024-09-24', 'Returned'), -- Hannah returned Little Red Riding Hood
(6, 2, '2024-09-14', '2024-09-19', 'Returned'), -- Lis returned Little Red Riding Hood
(6, 4, '2024-09-20', '2024-09-24', 'Returned'), -- Lis returned The Bro Code
(4, 8, '2024-09-20', '2024-09-24', 'Returned'), -- Edin returned The Old Man and The Sea
(2, 9, '2024-09-22', '2024-09-23', 'Returned'), -- Rron returned The 7 Habits of Highly Effective People
(5, 7, '2024-09-22', '2024-09-23', 'Returned'), -- Camila returned The Witness
(3, 9, '2024-09-10', '2024-09-12', 'Returned'), -- Hannah returned The 7 Habits of Highly Effective People
(4, 1, '2024-09-18', '2024-09-23', 'Returned'); -- Edin returned 48 Laws of Power

-- Adding reservation records
INSERT INTO Reservation (User_ID, Book_ID, Reservation_Date, Status) VALUES
(6, 1, '2024-09-20', 'Active'), -- Hannah reserves Kite Runner
(3, 5, '2024-09-20', 'Active');  -- Lis reserves 48 Laws of Power

-- Adding reviews`
INSERT INTO Review (User_ID, Book_ID, Review_Text, Rating, Review_Date) VALUES
(3, 2, 'Amazing kid`s book!', 5, '2024-09-25'), -- Hannah reviews Little Red Riding Hood
(6, 2, 'Great for Kids', 4, '2024-09-20'), -- Lis reviews Little Red Riding Hood
(6, 4, 'Hilarious!', 5, '2024-09-25'), -- Lis reviews The Bro Code
(4, 8, 'Very Good!', 5, '2024-09-25'), -- Edin reviews The Old Man and The Sea
(2, 9, 'Boring!', 3, '2024-09-25'), -- Rron reviews The 7 Habits of Highly Effective People
(5, 7, 'Great writing but some plot holes!', 4, '2024-09-25'), -- Camila reviews The Witness
(3, 9, 'Very Helpful!', 5, '2024-09-25'), -- Hannah reviews  The 7 Habits of Highly Effective People
(4, 1, 'This was very good writing!', 5, '2024-09-25'); -- Edin reviews 48 Laws of Power