import mysql.connector

# Conecta sem especificar banco
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Lara296082**",
    auth_plugin="mysql_native_password"
)

my_cursor = mydb.cursor()

# Cria banco, se não existir
my_cursor.execute("CREATE DATABASE IF NOT EXISTS gerenciamento_estoque")
my_cursor.execute("USE gerenciamento_estoque")

# Cria tabelas
my_cursor.execute("""
CREATE TABLE IF NOT EXISTS Usuarios (
    usuario_id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(50) NOT NULL,
    senha VARCHAR(20) NOT NULL,
    email VARCHAR(50) NOT NULL
)
""")

my_cursor.execute("""
CREATE TABLE IF NOT EXISTS Produtos (
    produto_id INT PRIMARY KEY AUTO_INCREMENT,
    imagem VARCHAR(50),
    nome_produto VARCHAR(100) NOT NULL,
    estoque VARCHAR(80) NOT NULL,
    descricao VARCHAR(300) NOT NULL,
    fornecedor VARCHAR(100) NOT NULL,
    criado_por VARCHAR(80) NOT NULL,
    criado_em DATE NOT NULL,
    atualizado_em DATE NOT NULL
)
""")

print("Banco e tabelas criados com sucesso!")
my_cursor.close()
mydb.close()
