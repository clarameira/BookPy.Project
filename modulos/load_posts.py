import sqlite3

def fetch_posts():
    with sqlite3.connect("BookpyLogin.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM posts")
        posts = cursor.fetchall()
    return posts