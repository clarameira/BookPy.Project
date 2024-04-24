import sqlite3

def savePost(post):
    try:
        with sqlite3.connect("BookpyLogin.db") as connection:
            cursor = connection.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts(         
                           Id INTEGER PRIMARY KEY AUTOINCREMENT,
                           Username TEXT NOT NULL,
                           Content TEXT NOT NULL,
                           Title TEXT,
                           Author TEXT,
                           Publisher TEXT
            )""")

            cursor.execute("INSERT INTO posts (Username, Content, Title, Author, Publisher) VALUES (?, ?, ?, ?, ?)", (post.user_author, post.content, post.title, post.author, post.publisher))
            
            connection.commit()

            return("Post salvo com sucesso!")

    except sqlite3.Error as e:
        print(f"Erro ao inserir dados no banco de dados: {e}")