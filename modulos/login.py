import sqlite3

def login(usuario, senha, email):
    try:
        with sqlite3.connect("BookpyLogin.db") as connection:
            cursor = connection.cursor()

            cursor.execute("SELECT Username, Password, Email FROM users")
            dados = cursor.fetchall()

            for linha in dados:
                if usuario == linha[0] and senha == linha[1] and email == linha[2]:    
                    connection.commit()
                    return "Usuário encontrado!"
                
                else:
                    continue

            connection.commit()
            return "Usuário não cadastrado"
    except sqlite3.Error as e:
        print(f"Erro ao inserir dados no banco de dados: {e}")