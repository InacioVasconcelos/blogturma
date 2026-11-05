import mysql.connector


class Conexao:
    def criar_conexao(self):
        cnx = mysql.connector.connect(
            host="127.0.0.1",
            port=3308,
            user="root",
            password="root",
            database="blog"
        )

        return cnx