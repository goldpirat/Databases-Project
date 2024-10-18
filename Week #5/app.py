from db_connection import get_db_connection
from books import list_books
from flask import Flask, render_template, request, redirect, url_for, flash, session
import hashlib

app = Flask(__name__, template_folder="templates", static_folder="templates/static")
app.secret_key = '&1\xedQ\xd8L7\x14\x8e\xf5\xe9\xf8\xcf\xad\xb6RK\xa5u\xe0\x13\xde\x18i'

@app.route("/books")
def books():
    book_data = list_books()
    print(book_data)
    return render_template("books.html", books=book_data)

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        # When a review is submitted
        user_id = 1  # Assuming the user is logged in and has user_id=1. Replace with session logic if available
        book_id = request.form['book_id']
        review_text = request.form['review']
        rating = request.form.get('rating', 5)  # Assuming a default rating of 5 stars
        
        # Insert the new review into the database
        cursor.execute("""
            INSERT INTO Review (User_ID, Book_ID, Review_Text, Rating, Review_Date)
            VALUES (%s, %s, %s, %s, NOW())
        """, (user_id, book_id, review_text, rating))
        conn.commit()

        flash('Review added successfully!')
        return redirect(url_for('reviews'))
    # Fetch reviews from the database
    cursor.execute("""
        SELECT U.Username, B.Title, R.Review_Text, R.Rating
        FROM Review R
        JOIN User U ON R.User_ID = U.User_ID
        JOIN Book B ON R.Book_ID = B.Book_ID
    """)
    reviews_data = cursor.fetchall()

    conn.close()
    return render_template('reviews.html', reviews=reviews_data)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Insert new user into the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if username or email already exists
        cursor.execute("SELECT * FROM User WHERE Username = %s OR Email = %s", (username, email))
        existing_user = cursor.fetchone()

        if existing_user:
            flash(f'Error: Username or Email already exists!', 'danger')
        else:
            try:
                cursor.execute("""
                    INSERT INTO User (Username, Email, Password, Role)
                    VALUES (%s, %s, %s, %s)
                """, (username, email, hashed_password, role))
                conn.commit()
                flash(f'User {username} has been added successfully!', 'success')
            except Exception as e:
                conn.rollback()
                flash(f'Error adding user: {str(e)}', 'danger')
            finally:
                cursor.close()
                conn.close()

        return redirect(url_for('add_user'))

    return render_template('add_user.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        # Retrieve form data
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        isbn = request.form['isbn']
        copies = int(request.form['copies'])  # Ensure copies is an integer
        
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Check if the book with the given ISBN already exists
            cursor.execute("SELECT Available_Copies FROM Book WHERE ISBN = %s", (isbn,))
            existing_book = cursor.fetchone()

            if existing_book:
                # If the book exists, update the available copies
                cursor.execute("""
                    UPDATE Book 
                    SET Available_Copies = Available_Copies + %s 
                    WHERE ISBN = %s
                """, (copies, isbn))
                flash(f'Updated copies of "{title}" by {copies} more.', 'success')
            else:
                # If the book doesn't exist, insert it as a new book
                cursor.execute("""
                    INSERT INTO Book (Title, Author, Genre, ISBN, Available_Copies)
                    VALUES (%s, %s, %s, %s, %s)
                """, (title, author, genre, isbn, copies))
                flash(f'Book "{title}" has been added successfully!', 'success')

            # Commit the transaction
            conn.commit()

        except Exception as e:
            conn.rollback()
            flash(f'Error adding or updating book: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()

        # Redirect to the same page to clear form
        return redirect(url_for('add_book'))

    # Render the form if GET request
    return render_template('add_book.html')


@app.route('/borrow_book', methods=['GET', 'POST'])
def borrow_books():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        user_id = request.form.get('user')
        book_id = request.form.get('book')

        # Insert the borrowing record
        cursor.execute("INSERT INTO Borrowing (User_ID, Book_ID, Borrow_Date, Status) VALUES (%s, %s, NOW(), 'Borrowed')", (user_id, book_id))
        
        # Decrease the available copies of the book by 1
        cursor.execute("UPDATE Book SET Available_Copies = Available_Copies - 1 WHERE Book_ID = %s AND Available_Copies > 0", (book_id,))
        
        conn.commit()  # Commit both the borrow record and the update to available copies
        
        flash('Successfully borrowed book for selected user.')
        return redirect(url_for('borrow_books'))

    cursor.execute("SELECT User_ID, Username FROM User")
    users = cursor.fetchall()

    cursor.execute("SELECT Book_ID, Title FROM Book WHERE Available_Copies > 0")
    books = cursor.fetchall()

    conn.close()

    return render_template('borrow_book.html', users=users, books=books)

@app.route('/return_book', methods=['GET', 'POST'])
def return_book():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        # Handle the return of the book using Borrowing_ID
        borrowing_id = request.form.get('borrowing_id')

        # Mark the book as returned and update available copies
        cursor.execute("""
            UPDATE Borrowing SET Status = 'Returned', Return_Date = NOW()
            WHERE Borrowing_ID = %s AND Status = 'Borrowed'
        """, (borrowing_id,))

        # Get the Book_ID associated with this borrowing record to update available copies
        cursor.execute("SELECT Book_ID FROM Borrowing WHERE Borrowing_ID = %s", (borrowing_id,))
        book_id = cursor.fetchone()[0]

        # Increase the available copies of the book
        cursor.execute("UPDATE Book SET Available_Copies = Available_Copies + 1 WHERE Book_ID = %s", (book_id,))
        conn.commit()

        flash('Book returned successfully.')
        return redirect(url_for('return_book'))

    # Fetch users who have borrowed books
    cursor.execute("""
        SELECT U.User_ID, U.Username
        FROM User U
        JOIN Borrowing B ON U.User_ID = B.User_ID
        WHERE B.Status = 'Borrowed'
        GROUP BY U.User_ID, U.Username
    """)
    users = cursor.fetchall()

    # Fetch borrowing records based on the selected user
    selected_user = request.args.get('user')
    books = []
    if selected_user:
        cursor.execute("""
            SELECT BR.Borrowing_ID, B.Title, BR.Borrow_Date
            FROM Book B
            JOIN Borrowing BR ON B.Book_ID = BR.Book_ID
            WHERE BR.User_ID = %s AND BR.Status = 'Borrowed'
        """, (selected_user,))
        books = cursor.fetchall()

    conn.close()

    return render_template('return_book.html', users=users, books=books, selected_user=selected_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT User_ID, Username, Role FROM User WHERE Email = %s AND Password = %s", (email, hashed_password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[2]
            flash(f'Welcome, {user[1]}!')

            if user[2] == 'Librarian':
                return redirect(url_for('maintenance'))  # Librarians are redirected to maintenance
            else:
                return redirect(url_for('profile'))  # Regular users are redirected to profile
        else:
            flash('Invalid credentials. Please try again.')

    return render_template('login.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check for duplicate email or username
        cursor.execute("SELECT * FROM User WHERE Email = %s OR Username = %s", (email, username))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('User with this email or username already exists.')
        else:
            cursor.execute("""
                INSERT INTO User (Username, Email, Password, Role)
                VALUES (%s, %s, %s, %s)
            """, (username, email, hashed_password, role))
            conn.commit()
            flash('Registration successful. Please login.')
            return redirect(url_for('login'))

        conn.close()

    return render_template('register.html')

# Profile route (protected)
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Please login to access your profile.')
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch user details
    cursor.execute("SELECT Username, Email, Role FROM User WHERE User_ID = %s", (user_id,))
    user = cursor.fetchone()

    # Fetch user's borrowed books
    cursor.execute("""
        SELECT B.Title, BR.Borrow_Date
        FROM Borrowing BR
        JOIN Book B ON BR.Book_ID = B.Book_ID
        WHERE BR.User_ID = %s AND BR.Status = 'Borrowed'
    """, (user_id,))
    borrowed_books = cursor.fetchall()

    # Fetch user's active reservations
    cursor.execute("""
        SELECT B.Title, R.Reservation_Date
        FROM Reservation R
        JOIN Book B ON R.Book_ID = B.Book_ID
        WHERE R.User_ID = %s AND R.Status = 'Active'
    """, (user_id,))
    reservations = cursor.fetchall()

    # Fetch user's reviews
    cursor.execute("""
        SELECT B.Title, R.Rating, R.Review_Text
        FROM Review R
        JOIN Book B ON R.Book_ID = B.Book_ID
        WHERE R.User_ID = %s
    """, (user_id,))
    reviews = cursor.fetchall()

    conn.close()

    return render_template(
        'profile.html', 
        user={'username': user[0], 'email': user[1], 'role': user[2]},
        borrowed_books=borrowed_books,
        reservations=reservations,
        reviews=reviews
    )


# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.')
    return redirect(url_for('login'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/imprint')
def imprint():
    return render_template('imprint.html')

@app.route('/maintenance')
def maintenance():
    return render_template('maintenance.html')

if __name__ == '__main__':
    app.run(debug=True)