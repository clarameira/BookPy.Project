import sqlite3

def delete_data(post_id, user):
    try:
        with sqlite3.connect("BookpyLogin.db") as connection:
            cursor = connection.cursor()

            cursor.execute("DELETE FROM posts WHERE Id = ? AND Username = ?", (post_id, user,))

            connection.commit()

            return("Post removido com sucesso!")

    except sqlite3.Error as e:
        print(f"Erro ao remover dados no banco de dados: {e}")