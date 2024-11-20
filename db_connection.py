import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_connection():
    conn = mysql.connector.MySQLConnection(
        host=os.environ.get("SQL_HOST"),
        user=os.environ.get("SQL_USER"),
        port=int(os.environ.get("SQL_PORT")),
        password=os.environ.get("SQL_PASSWORD"),
        database=os.environ.get("SQL_DATABASE"),
    )
    conn.connect()
    return conn

def prepare_tables():
    conn = get_db_connection()
    
    queries = """
        CREATE TABLE IF NOT EXISTS User (
        User_ID INT AUTO_INCREMENT PRIMARY KEY,
        Username VARCHAR(255) UNIQUE NOT NULL,
        Email VARCHAR(255) UNIQUE NOT NULL,
        Password VARCHAR(255) NOT NULL,  -- Passwords will be hashed
        Role ENUM('Librarian', 'Regular User') NOT NULL,
        created_at DATE DEFAULT CURRENT_DATE
    );
    
    CREATE TABLE IF NOT EXISTS Book (
        Book_ID INT AUTO_INCREMENT PRIMARY KEY,
        Title VARCHAR(255) NOT NULL,
        Author VARCHAR(255),
        Genre VARCHAR(100),
        ISBN VARCHAR(13) UNIQUE,
        Available_Copies INT DEFAULT 1 CHECK (Available_Copies >= 0),
        Rating FLOAT CHECK (Rating BETWEEN 0 AND 5),
        Description VARCHAR(1400) DEFAULT 'This book has not been reviewed by the library yet.'
    );
    -- Table for borrowing records
    CREATE TABLE IF NOT EXISTS Borrowing (
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
    CREATE TABLE IF NOT EXISTS Reservation (
        Reservation_ID INT AUTO_INCREMENT PRIMARY KEY,
        User_ID INT,
        Book_ID INT,
        Reservation_Date DATE NOT NULL,
        Status ENUM('Active', 'Completed') DEFAULT 'Active',
        FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON DELETE CASCADE,
        FOREIGN KEY (Book_ID) REFERENCES Book(Book_ID) ON DELETE CASCADE,
        UNIQUE (User_ID, Book_ID)
    );
    -- Table for reviews and ratings
    CREATE TABLE IF NOT EXISTS Review (
        Review_ID INT AUTO_INCREMENT PRIMARY KEY,
        User_ID INT,
        Book_ID INT,
        Review_Text TEXT,
        Rating INT CHECK (Rating BETWEEN 1 AND 5),
        Review_Date DATE NOT NULL,
        FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON DELETE CASCADE,
        FOREIGN KEY (Book_ID) REFERENCES Book(Book_ID) ON DELETE CASCADE,
        UNIQUE (User_ID, Book_ID)
    );
    -- Table for account management (tracking profile edits)
    CREATE TABLE IF NOT EXISTS Account_Management (
        Account_ID INT AUTO_INCREMENT PRIMARY KEY,
        User_ID INT,
        Profile_Edit_Date DATE,
        FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON DELETE CASCADE
    );
    -- Table for genres (optional)
    CREATE TABLE IF NOT EXISTS Genre (
        Genre_ID INT AUTO_INCREMENT PRIMARY KEY,
        Genre_Name VARCHAR(100) NOT NULL
    );
    -- Table to link books and genres
    CREATE TABLE IF NOT EXISTS Book_Genre (
        Book_ID INT,
        Genre_ID INT,
        PRIMARY KEY (Book_ID, Genre_ID),
        FOREIGN KEY (Book_ID) REFERENCES Book(Book_ID) ON DELETE CASCADE,
        FOREIGN KEY (Genre_ID) REFERENCES Genre(Genre_ID) ON DELETE CASCADE
    );
    
    INSERT INTO User (User_ID, Username, Email, Password, Role) VALUES
    (1, 'Flori Kusari', 'fkusari@constructor.university', 'hashed_password', 'Librarian'),
    (2, 'Rron Dermaku', 'rdermaku@constructor.university', 'hashed_password', 'Regular User'),
    (3, 'Hannah Paulus', 'hpaulus@constructor.university', 'hashed_password', 'Regular User'),
    (4, 'Edin Berisha', 'eberisha@constructor.university', 'hashed_password', 'Regular User'),
    (5, 'Camila Pina Pinto', 'cpinto@constructor.university', 'hashed_password', 'Regular User'),
    (6, 'Lis Fazliu', 'lfazliu@constructor.university', 'hashed_password', 'Regular User');
    
    
    INSERT INTO Book (Book_ID, Title, Author, Genre, ISBN, Available_Copies, Description) VALUES
    (1, '48 Laws of Power', 'Robert Greene', 'Philosophy', '9780140280197', 2, 'A book about power dynamics.'),
    (2, 'Little Red Riding Hood (Keepsake Stories)', 'N/A', 'Children', '9781577681984', 15, "A classic children's tale."),
    (3, 'The Bro Code', 'Barney Stinson - Matt Kuhn', 'Humor', '9781439110003', 32, 'Rules for bros.'),
    (4, 'The Kite Runner', 'Khaled Hosseini', 'Drama', '9781594631931', 14, 'A powerful story of redemption.'),
    (5, 'The Laws of Human Nature', 'Robert Greene', 'Philosophy', '9781781259191', 8, 'A deep dive into human psychology.'),
    (6, 'The Witness', 'Sandra Brown', 'Thriller', '9781455538263', 7, 'A gripping thriller.'),
    (7, 'The Old Man and The Sea', 'Ernest Hemingway', 'Adventure', '9798329875195', 5, 'A tale of struggle and triumph.'),
    (8, 'The 7 Habits of Highly Effective People: 30th Anniversary Edition', 'Stephen R. Covey', 'Self-help', '9781982137274', 4, 'A classic self-help book.');
    
    
    INSERT INTO Borrowing (User_ID, Book_ID, Borrow_Date, Return_Date, Status) VALUES
    (3, 2, '2024-09-20', '2024-09-24', 'Returned'),
    (6, 2, '2024-09-14', '2024-09-19', 'Returned'),
    (6, 3, '2024-09-20', '2024-09-24', 'Returned'),
    (4, 7, '2024-09-20', '2024-09-24', 'Returned'),
    (2, 8, '2024-09-22', '2024-09-23', 'Returned'),
    (5, 6, '2024-09-22', '2024-09-23', 'Returned'),
    (3, 8, '2024-09-10', '2024-09-12', 'Returned'),
    (4, 1, '2024-09-18', '2024-09-23', 'Returned');
    
    
    INSERT INTO Reservation (User_ID, Book_ID, Reservation_Date, Status) VALUES
    (6, 4, '2024-09-20', 'Active'),
    (3, 5, '2024-09-20', 'Active');
    
    INSERT INTO Review (User_ID, Book_ID, Review_Text, Rating, Review_Date) VALUES
    (3, 2, "Amazing kid's book!", 5, '2024-09-25'),
    (6, 2, 'Great for Kids', 4, '2024-09-20'),
    (6, 3, 'Hilarious!', 5, '2024-09-25'),
    (4, 7, 'Very Good!', 5, '2024-09-25'),
    (2, 8, 'Boring!', 3, '2024-09-25'),
    (5, 6, 'Great writing but some plot holes!', 4, '2024-09-25'),
    (3, 8, 'Very Helpful!', 5, '2024-09-25'),
    (4, 1, 'This was very good writing!', 5, '2024-09-25');
    
    """
    try:
        cursor = conn.cursor()
        for query in queries.strip().split(';'):
            if query.strip():
                cursor.execute(query)
        conn.commit()
        print("Created tables(if they did not exist)")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()

prepare_tables()
