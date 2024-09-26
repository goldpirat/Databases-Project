-- Adding more users
INSERT INTO User (Name, Email) VALUES
('Flori Kusari', 'fkusari@constructor.university'),
('Rron Dermaku', 'rdermaku@constructor.university'),
('Hannah Paulus', 'hpaulus@constructor.university'),
('Lis Fazliu', 'lfazliu@constructor.university');

-- Adding more regular users and librarians
INSERT INTO Librarian (User_ID) VALUES (1);     -- Flori is a librarian
INSERT INTO Regular_User (User_ID) VALUES (2);  -- Rron is a regular user
INSERT INTO Regular_User (User_ID) VALUES (3);  -- Hannah is a regular user
INSERT INTO Regular_User (User_ID) VALUES (4);  -- Lis is a Regular user

-- Adding more books
INSERT INTO Book (Title, Author, ISBN, Available_Copies) VALUES
('48 Laws of Power', 'Robert Greene', '9780140280197', 2),
('The Laws of Human Nature', 'Robert Greene', '9781781259191', 8),
('The Witness', 'Sandra Brown', '9781455538263', 7),
('The Old Man and the Sea', 'Ernest Hemingway', '9798329875195', 5),
('The 7 Habits of Highly Effective People: 30th Anniversary Edition', 'Stephen R. Covey', '781982137274', 4);

-- Adding borrowing records
INSERT INTO Borrowing (User_ID, Book_ID, Borrow_Date, Return_Date, Status) VALUES
(3, 2, '2024-09-20', '2024-09-24', 'Returned'),
(4, 1, '2024-09-18', '2024-09-23', 'Returned');

-- Adding reservation records
INSERT INTO Reservation (User_ID, Book_ID, Reservation_Date, Status) VALUES
(4, 1, '2024-09-20', 'Active');  -- Lis reserves '48 Laws of Power'

-- Adding reviews
INSERT INTO Review (User_ID, Book_ID, Review_Text, Rating, Review_Date) VALUES
(3, 2, 'Amazing book!', 5, '2024-09-25'),  -- Hannah reviews 'The Laws of Human Nature'
(4, 3, 'A timeless classic.', 4, '2024-09-24');  -- Lis reviews 'The Witness'