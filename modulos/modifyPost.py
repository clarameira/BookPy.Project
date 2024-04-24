import sqlite3

def modify_data(post_entries, user, id):
    if(post_entries.content == None or post_entries.content =="" or post_entries.content == "Escreva aqui o que deseja postar..."):
        return("Você precisa adicionar uma postagem!")
    
    try:
        with sqlite3.connect("BookpyLogin.db") as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE posts SET Title = ?, Author = ?, Publisher = ?, Content = ? WHERE Id = ? AND Username = ?", (post_entries.title, post_entries.author, post_entries.publisher, post_entries.content, id, user))
            connection.commit()

            return("Post modificado com sucesso!")
        
    except sqlite3.Error as e:
        print(f"Erro ao modificar dados no banco de dados: {e}")