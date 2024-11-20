from db_connection import get_db_connection
def list_books():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT Book_ID, Title, Author, Genre, ISBN, Available_Copies FROM Book")
        results = cursor.fetchall()
        return results
