-- Table for storing book information
CREATE TABLE Book (
    Book_ID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    Author VARCHAR(255),
    ISBN VARCHAR(13) UNIQUE,  -- ISBN is always unique
    Available_Copies  INT DEFAULT 1 CHECK (Available_Copies >= 0)
);

-- Base table for storing user information
CREATE TABLE User (
    User_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL
);

-- Regular_User table inheriting from User
CREATE TABLE Regular_User (
    User_ID INT PRIMARY KEY, 
    FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON DELETE CASCADE
);

-- Librarian table inheriting from User
CREATE TABLE Librarian (
    User_ID INT PRIMARY KEY,  -- Inherits the primary key from User
    FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON DELETE CASCADE
);

-- Table for borrowing records
CREATE TABLE Borrowing (
    Borrowing_ID INT AUTO_INCREMENT PRIMARY KEY,
    User_ID INT,
    Book_ID INT,
    Borrow_Date DATE NOT NULL,
    Return_Date DATE,
    Status ENUM('Borrowed', 'Returned') DEFAULT 'Borrowed',
    FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON DELETE CASCADE,
    FOREIGN KEY (Book_ID) REFERENCES Book(Book_ID) ON DELETE CASCADE
);

-- Table for reservation records
CREATE TABLE Reservation (
    Reservation_ID INT AUTO_INCREMENT PRIMARY KEY,
    User_ID INT,
    Book_ID INT,
    Reservation_Date DATE NOT NULL,
    Status ENUM('Active', 'Completed') DEFAULT 'Active',  
    FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON DELETE CASCADE,
    FOREIGN KEY (Book_ID) REFERENCES Book(Book_ID) ON DELETE CASCADE
);

-- Table for storing reviews and ratings by users
CREATE TABLE Review (
    Review_ID INT AUTO_INCREMENT PRIMARY KEY,
    User_ID INT,
    Book_ID INT,
    Review_Text TEXT,
    Rating INT CHECK (Rating BETWEEN 1 AND 5),
    Review_Date DATE NOT NULL,
    FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON DELETE CASCADE,
    FOREIGN KEY (Book_ID) REFERENCES Book(Book_ID) ON DELETE CASCADE,
    UNIQUE (User_ID, Book_ID)  -- Only one review per user
);

-- Table for tracking user accounts and managing profile edits
CREATE TABLE Account_Management (
    Account_ID INT AUTO_INCREMENT PRIMARY KEY,
    User_ID INT,
    Profile_Edit_Date DATE,
    FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON DELETE CASCADE
);
