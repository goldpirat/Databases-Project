from db_connection import get_db_connection
from books import list_books
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from ip_functions import parse_access_logs, parse_error_logs, plot_access_timeline, plot_error_timeline
import re
import requests
from werkzeug.security import generate_password_hash, check_password_hash
import bleach
import os
import mysql.connector


app = Flask(__name__, template_folder="templates", static_folder="templates/static")
app.secret_key = os.environ.get('SECRET_KEY', 'your_default_secret_key')

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Input validation patterns
USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_]{8,30}$')
PASSWORD_PATTERN = re.compile(r'^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,}$')
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

def validate_input(username, password, email):
    if not USERNAME_PATTERN.match(username):
        return False, "Username must be 8-30 characters long and contain only letters, numbers, and underscores."
    if not PASSWORD_PATTERN.match(password):
        return False, "Password must be at least 8 characters long, include 1 uppercase letter, 1 number, and 1 special character."
    if not EMAIL_PATTERN.match(email):
        return False, "Invalid email format."
    return True, "Valid input."

def librarian_required(f):
    """Decorator to ensure the user is a librarian."""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'Librarian':
            flash('Unauthorized access. Librarian credentials required.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/access_stats')
@librarian_required
def access_stats():
    access_data = parse_access_logs("/var/log/apache2/access.log")

    # Format the data for better readability
    formatted_data = []
    for entry in access_data['raw_data']:
        formatted_entry = {
            'ip': entry['ip'],
            'datetime': entry['datetime'].strftime('%Y-%m-%d %H:%M:%S'),
            'request_method': entry['request_method'],
            'url': entry['url'],
            'status': entry['status'],
            'user_agent': entry['user_agent']
        }
        formatted_data.append(formatted_entry)

    return jsonify({
        'total_entries': len(formatted_data),
        'logs': formatted_data,
        'page_counts': access_data['page_counts'],
        'browser_stats': access_data['browser_stats']
    })

@app.route('/error_stats')
@librarian_required
def error_stats():
    error_data = parse_error_logs("/var/log/apache2/error.log")

    # Format the data for better readability
    formatted_data = []
    for entry in error_data['raw_data']:
        formatted_entry = {
            'datetime': entry['datetime'].strftime('%Y-%m-%d %H:%M:%S'),
            'level': entry['level'],
            'client_ip': entry['client_ip'],
            'message': entry['message']
        }
        formatted_data.append(formatted_entry)

    return jsonify({
        'total_entries': len(formatted_data),
        'logs': formatted_data,
        'error_stats': error_data['error_stats']
    })


@app.route('/location')
@librarian_required
def location():
    access_data = parse_access_logs("/var/log/apache2/access.log")
    ip_list = list(set(access_data['ip_access'].keys()))

    if not ip_list:
        return render_template('location.html', 
                               ip_list=ip_list,
                               error="No IPs found in access logs")

    location_details = []

    for ip in ip_list:
        try:
            response = requests.get(f'https://ipinfo.io/{ip}/json')
            response.raise_for_status()  # Raise an HTTPError for bad responses
            location_data = response.json()

            loc = location_data.get('loc', '0,0').split(',')
            latitude, longitude = float(loc[0]), float(loc[1])

            location_details.append({
                "ip": ip,
                "latitude": latitude,
                "longitude": longitude,
                "city": location_data.get('city', 'Unknown'),
                "region": location_data.get('region', 'Unknown'),
                "country": location_data.get('country', 'Unknown')
            })

        except requests.exceptions.RequestException as e:
            continue  # Skip IP if there's a request error

    return render_template('location.html', 
                           ip_list=ip_list,
                           location_details=location_details)




@app.route('/view_logs')
@librarian_required
def view_logs():
    # Parse logs
    access_data = parse_access_logs("/var/log/apache2/access.log")
    error_data = parse_error_logs("/var/log/apache2/error.log")

    # Generate visualizations
    plot_access_timeline(access_data)
    plot_error_timeline(error_data)

    # Prepare IP statistics for template
    ip_stats = {}
    for ip, timestamps in access_data['ip_access'].items():
        ip_stats[ip] = {
            'count': len(timestamps),
            'last_access': max(timestamps).strftime('%Y-%m-%d %H:%M:%S')
        }

    return render_template('logs.html', ip_stats=ip_stats)

@app.route('/books')
def books():
    conn = get_db_connection()
    cursor = conn.cursor()  # Create the cursor without 'with'

    try:
        cursor.execute("SELECT * FROM Book")
        books = cursor.fetchall()
    except Exception as e:
        print(f"An error occurred: {e}")
        books = []
    finally:
        cursor.close()  # Explicitly close the cursor
        conn.close()  # Close the connection

    return render_template("books.html", books=books)

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if 'user_id' not in session:
        flash('Please login to access reviews.')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        # When a review is submitted
        user_id = session['user_id']
        book_id = request.form['book_id']
        review_text = bleach.clean(request.form['review'])
        rating = int(request.form.get('rating', 5))  # Assuming a default rating of 5 stars

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
@librarian_required
def add_user():
    if request.method == 'POST':
        # Get form data
        username = bleach.clean(request.form['username'].strip())
        email = bleach.clean(request.form['email'].strip())
        password = request.form['password']
        role = request.form['role']

        # Validate inputs
        is_valid, message = validate_input(username, password, email)
        if not is_valid:
            flash(message)
            return redirect(url_for('add_user'))

        hashed_password = generate_password_hash(password)

        # Insert new user into the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if username or email already exists
        cursor.execute("SELECT * FROM User WHERE Username = %s OR Email = %s", (username, email))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Error: Username or Email already exists!', 'danger')
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
@librarian_required
def add_book():
    if request.method == 'POST':
        # Retrieve form data
        title = bleach.clean(request.form['title'].strip())
        author = bleach.clean(request.form['author'].strip())
        genre = bleach.clean(request.form['genre'].strip())
        isbn = bleach.clean(request.form['isbn'].strip())
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
@librarian_required
def borrow_books():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        user_id = request.form.get('user')
        book_id = request.form.get('book')

        try:
            # Insert the borrowing record
            cursor.execute("""
                INSERT INTO Borrowing (User_ID, Book_ID, Borrow_Date, Status) 
                VALUES (%s, %s, NOW(), 'Borrowed')
            """, (user_id, book_id))

            # Decrease the available copies of the book by 1
            cursor.execute("""
                UPDATE Book SET Available_Copies = Available_Copies - 1 
                WHERE Book_ID = %s AND Available_Copies > 0
            """, (book_id,))

            conn.commit()  # Commit both the borrow record and the update to available copies

            flash('Successfully borrowed book for selected user.')
        except Exception as e:
            conn.rollback()
            flash(f'Error borrowing book: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('borrow_books'))

    cursor.execute("SELECT User_ID, Username FROM User")
    users = cursor.fetchall()

    cursor.execute("SELECT Book_ID, Title FROM Book WHERE Available_Copies > 0")
    books = cursor.fetchall()

    conn.close()

    return render_template('borrow_book.html', users=users, books=books)

@app.route('/return_book', methods=['GET', 'POST'])
@librarian_required
def return_book():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        # Handle the return of the book using Borrowing_ID
        borrowing_id = request.form.get('borrowing_id')

        try:
            # Mark the book as returned and update available copies
            cursor.execute("""
                UPDATE Borrowing SET Status = 'Returned', Return_Date = NOW()
                WHERE Borrowing_ID = %s AND Status = 'Borrowed'
            """, (borrowing_id,))

            # Get the Book_ID associated with this borrowing record to update available copies
            cursor.execute("SELECT Book_ID FROM Borrowing WHERE Borrowing_ID = %s", (borrowing_id,))
            book_id_result = cursor.fetchone()

            if book_id_result:
                book_id = book_id_result[0]
                # Increase the available copies of the book
                cursor.execute("""
                    UPDATE Book SET Available_Copies = Available_Copies + 1 
                    WHERE Book_ID = %s
                """, (book_id,))
                conn.commit()
                flash('Book returned successfully.')
            else:
                flash('Invalid borrowing record.', 'danger')
        except Exception as e:
            conn.rollback()
            flash(f'Error returning book: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()

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
@limiter.limit("10/minute")  # Limit login attempts
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT User_ID, Username, Password, Role FROM User WHERE Email = %s", 
                (email,)
            )
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user and check_password_hash(user[2], password):
                session['user_id'] = user[0]
                session['username'] = user[1]
                session['role'] = user[3]
                flash(f'Welcome, {user[1]}!')

                if user[3] == 'Librarian':
                    return redirect(url_for('maintenance'))
                else:
                    return redirect(url_for('profile'))
            else:
                flash('Invalid credentials. Please try again.')

        except Exception as err:
            flash('An error occurred. Please try again later.')
            print(f"Database error: {err}")  # Log the actual error securely

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("5/hour")  # Limit registration attempts
def register():
    if request.method == 'POST':
        # Sanitize inputs
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', '').strip()

        # Validate inputs
        is_valid, message = validate_input(username, password, email)
        if not is_valid:
            flash(message)
            return render_template('register.html')

        # Librarian key validation
        if role == 'Librarian':
            librarian_key = request.form.get('librarian_key', '')
            LIBRARIAN_REGISTRATION_KEY = os.environ.get('LIBRARIAN_KEY')
            if librarian_key != LIBRARIAN_REGISTRATION_KEY:
                flash('Invalid librarian registration key.')
                return render_template('register.html')

        # Hash password securely
        hashed_password = generate_password_hash(password)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Check for existing user
            cursor.execute("SELECT * FROM User WHERE Email = %s OR Username = %s", 
                           (email, username))
            existing_user = cursor.fetchone()

            if existing_user:
                flash('User with this email or username already exists.')
            else:
                # Insert new user
                cursor.execute("""
                    INSERT INTO User (Username, Email, Password, Role)
                    VALUES (%s, %s, %s, %s)
                """, (username, email, hashed_password, role))
                conn.commit()
                flash('Registration successful. Please login.')
                return redirect(url_for('login'))

        except Exception as err:
            flash(f'An error occurred. Please try again later.{err}')
            print(f"Database error: {err}")  # Log the actual error securely

        finally:
            cursor.close()
            conn.close()

    return render_template('register.html')


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

@app.route('/search_books', methods=['GET'])
def search_books():
    if 'user_id' not in session:
        flash('Please log in to search books')
        # Store the intended destination
        session['next'] = url_for('search_books')
        return redirect(url_for('login'))

    search_term = request.args.get('search_term')

    # If no search term, show the search form
    if not search_term:
        return render_template('search_books.html')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Searching both title and genre
    query = """
    SELECT Title, Author, Genre, ISBN, Available_Copies
    FROM Book
    WHERE LOWER(Title) LIKE LOWER(%s) 
    OR LOWER(Genre) LIKE LOWER(%s)
    """
    search_pattern = f'%{search_term}%'
    cursor.execute(query, (search_pattern, search_pattern))
    books = cursor.fetchall()

    conn.close()

    return render_template('search_books_results.html', books=books, search_term=search_term)

@app.route('/get_book_titles', methods=['GET'])
def get_book_titles():
    term = request.args.get('term', '')
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    SELECT Title FROM Book
    WHERE Title LIKE %s
    LIMIT 10
    """
    search_pattern = f'%{term}%'
    cursor.execute(query, (search_pattern,))
    books = cursor.fetchall()
    conn.close()

    # Extract titles from the fetched data
    book_titles = [book[0] for book in books]

    return jsonify(book_titles)


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

@app.route('/maintenance', methods=['GET', 'POST'])
@librarian_required
def maintenance():
    # Proceed to maintenance page
    return render_template('maintenance.html')

@app.route('/delete_user', methods=['GET'])
@librarian_required
def delete_user_page():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT User_ID, Username, Email FROM User")
    users = cursor.fetchall()
    conn.close()
    return render_template('delete_user.html', users=users)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
@librarian_required
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM User WHERE User_ID = %s", (user_id,))
        conn.commit()
        flash('User deleted successfully.', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error deleting user: {str(e)}', 'danger')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('delete_user_page'))

@app.route('/delete_books', methods=['GET'])
@librarian_required
def delete_books_page():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Book_ID, Title, Available_Copies FROM Book WHERE Available_Copies > 0")
    books = cursor.fetchall()
    conn.close()
    return render_template('delete_books.html', books=books)

@app.route('/delete_books', methods=['POST'])
@librarian_required
def delete_books():
    book_id = request.form.get('book_id', type=int)
    copies_to_delete = request.form.get('copies_to_delete', type=int)

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Reduce the available copies
        cursor.execute("""
            UPDATE Book SET Available_Copies = Available_Copies - %s
            WHERE Book_ID = %s AND Available_Copies >= %s
        """, (copies_to_delete, book_id, copies_to_delete))
        
        # Check if available copies are now 0, and delete the book if so
        cursor.execute("SELECT Available_Copies FROM Book WHERE Book_ID = %s", (book_id,))
        available_copies = cursor.fetchone()[0]
        
        if available_copies == 0:
            cursor.execute("DELETE FROM Book WHERE Book_ID = %s", (book_id,))

        conn.commit()
        flash('Book copies updated successfully.', 'success')

    except Exception as e:
        conn.rollback()
        flash(f'Error updating book copies: {str(e)}', 'danger')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('delete_books_page'))

if __name__ == '__main__':
    app.run(host='5.75.182.107', port=8010, debug=True)
