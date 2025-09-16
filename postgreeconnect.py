from flask import Flask
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# URL do banco do Render
DB_URL = "postgresql://gerenciamento_estoque_user:sIH2DLhlXQUBpZkNzQy776wQWBakhJAj@dpg-d32bqh7diees738lc0-a.oregon-postgres.render.com/gerenciamento_estoque"

# Nome do banco que você quer criar
NEW_DB_NAME = "meu_novo_banco"

# Criar app Flask
app = Flask(__name__)

def create_db():
    # Conecta no banco "gerenciamento_estoque" para poder criar outro
    conn = psycopg2.connect(
        host="dpg-d32bqh7diees738lc8d0-a.oregon-postgres.render.com",
        database="gerenciamento_estoque",
        user="gerenciamento_estoque_user",
        password="sIH2DLhlXQUBpZkNzQy776wQWBakhJAj",
        port=5432,
        sslmode='require'  # Força SSL
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    # Cria o banco se não existir
    try:
        cur.execute(f"CREATE DATABASE {NEW_DB_NAME}")
        print(f"Banco '{NEW_DB_NAME}' criado com sucesso!")
    except psycopg2.errors.DuplicateDatabase:
        print(f"O banco '{NEW_DB_NAME}' já existe.")

    cur.close()
    conn.close()

@app.route('/')
def index():
    return "Flask está rodando e o banco já foi criado/conectado!"

if __name__ == '__main__':
    create_db()
    app.run(debug=True)
