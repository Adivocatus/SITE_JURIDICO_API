import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="127.0.0.1",          # ou IP do servidor MySQL
        user="root",        # usuário do MySQL
        password="",      # senha do MySQL
        database="site_juridico_banco"  # nome do banco de dados
    )
