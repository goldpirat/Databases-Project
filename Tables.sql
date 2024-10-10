-- Table for storing user information
CREATE TABLE User (
    User_ID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(255) UNIQUE NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,  -- Passwords will be hashed
    Role ENUM('Librarian', 'Regular User') NOT NULL  -- Defining roles for Librarian and Regular users
);

-- Table for storing book information with a description field
CREATE TABLE Book (
    Book_ID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    Author VARCHAR(255),
    Genre VARCHAR(100),
    ISBN VARCHAR(13) UNIQUE,  -- ISBN is unique for each book
    Available_Copies INT DEFAULT 1 CHECK (Available_Copies >= 0),  -- Number of available copies, must be non-negative
    Rating FLOAT CHECK (Rating BETWEEN 0 AND 5),  -- Rating between 0 and 5 stars
    Description VARCHAR(1400) DEFAULT 'This book has not been reviewed by the library yet.'  -- Default description
);

-- Table for borrowing records
CREATE TABLE Borrowing (
    Borrowing_ID INT AUTO_INCREMENT PRIMARY KEY,
    User_ID INT,
    Book_ID INT,
    Borrow_Date DATE NOT NULL,
    Return_Date DATE,
    Status ENUM('Borrowed', 'Returned') DEFAULT 'Borrowed',
    FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON DELETE CASCADE,  -- When a user is deleted, their borrowing records are also deleted
    FOREIGN KEY (Book_ID) REFERENCES Book(Book_ID) ON DELETE CASCADE  -- When a book is deleted, its borrowing records are also deleted
);

-- Table for reservation records
CREATE TABLE Reservation (
    Reservation_ID INT AUTO_INCREMENT PRIMARY KEY,
    User_ID INT,
    Book_ID INT,
    Reservation_Date DATE NOT NULL,
    Status ENUM('Active', 'Completed') DEFAULT 'Active',
    FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON DELETE CASCADE,
    FOREIGN KEY (Book_ID) REFERENCES Book(Book_ID) ON DELETE CASCADE,
    UNIQUE (User_ID, Book_ID)  -- Prevent users from reserving the same book more than once
);

-- Table for reviews and ratings
CREATE TABLE Review (
    Review_ID INT AUTO_INCREMENT PRIMARY KEY,
    User_ID INT,
    Book_ID INT,
    Review_Text TEXT,
    Rating INT CHECK (Rating BETWEEN 1 AND 5),  -- Ratings must be between 1 and 5
    Review_Date DATE NOT NULL,
    FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON DELETE CASCADE,
    FOREIGN KEY (Book_ID) REFERENCES Book(Book_ID) ON DELETE CASCADE,
    UNIQUE (User_ID, Book_ID)  -- A user can review a book only once
);

-- Table for account management (tracking profile edits)
CREATE TABLE Account_Management (
    Account_ID INT AUTO_INCREMENT PRIMARY KEY,
    User_ID INT,
    Profile_Edit_Date DATE,
    FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON DELETE CASCADE
);

-- Table for genres (optional, for extended functionality)
CREATE TABLE Genre (
    Genre_ID INT AUTO_INCREMENT PRIMARY KEY,
    Genre_Name VARCHAR(100) NOT NULL
);

-- Table to link books and genres (many-to-many relationship)
CREATE TABLE Book_Genre (
    Book_ID INT,
    Genre_ID INT,
    PRIMARY KEY (Book_ID, Genre_ID),
    FOREIGN KEY (Book_ID) REFERENCES Book(Book_ID) ON DELETE CASCADE,
    FOREIGN KEY (Genre_ID) REFERENCES Genre(Genre_ID) ON DELETE CASCADE
);
