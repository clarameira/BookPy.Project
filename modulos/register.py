import sqlite3

def insert_into_database(login, email, senha):
    try:
        with sqlite3.connect("BookpyLogin.db") as connection:
            cursor = connection.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(         
                Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL,
                Email TEXT NOT NULL,
                Password TEXT NOT NULL     
            )""")

            cursor.execute("SELECT Username, Email FROM users")
            resultados = cursor.fetchall()

            for linha in resultados:
                if login != linha[0] and email != linha[1]:
                    continue
                else:
                    return "Usuário já cadastrado"
            cursor.execute("INSERT INTO users (Username, Email, Password) VALUES (?, ?, ?)", (login, email, senha))
            
            # Commit para salvar as alterações
            connection.commit()
            return("Usuário cadastrado com sucesso!")

    except sqlite3.Error as e:
        print(f"Erro ao inserir dados no banco de dados: {e}")