import psycopg2

try:
    conn = psycopg2.connect(
        host="dpg-d32bqh7diees738lc0-a.oregon-postgres.render.com",
        database="gerenciamento_estoque",
        user="gerenciamento_estoque_user",
        password="sIH2DLhlXQUBpZkNzQy776wQWBakhJAj",
        port=5432,
        sslmode="require"
    )
    print("Conexão bem-sucedida!")
    conn.close()
except Exception as e:
    print("Erro ao conectar:", e)