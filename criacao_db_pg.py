import psycopg2

# Conecta direto no banco já existente (Render não deixa criar outro banco)
conn = psycopg2.connect(
    host="dpg-d32bqh7diees738lc8d0-a.oregon-postgres.render.com",
    port=5432,
    database="gerenciamento_estoque",
    user="gerenciamento_estoque_user",
    password="sIH2DLhlXQUBpZkNzQy776wQWBakhJAj"
)

cursor = conn.cursor()

# Cria tabelas (sem CREATE DATABASE, só tabelas mesmo)
cursor.execute("""
CREATE TABLE IF NOT EXISTS Usuarios (
    usuario_id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    senha VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Produtos (
    produto_id SERIAL PRIMARY KEY,
    imagem TEXT,
    nome_produto VARCHAR(100) NOT NULL,
    estoque INTEGER NOT NULL,
    descricao TEXT NOT NULL,
    fornecedor VARCHAR(100) NOT NULL,
    criado_por VARCHAR(50),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
cursor.close()
conn.close()

print("✅ Tabelas criadas com sucesso no PostgreSQL Render!")
