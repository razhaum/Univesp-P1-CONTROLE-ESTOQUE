import mysql.connector

mydb = mysql.connector.connect(
    host ="localhost",
    user = "root",
    passwd = "110719",
    auth_plugin = "mysql_native_password",
    database = "gerenciamento_estoque")

my_cursor = mydb.cursor()


#Cria o banco de dado
my_cursor.execute("CREATE DATABASE IF NOT EXISTS gerenciamento_estoque")

#Cria as tabelas

my_cursor.execute("CREATE TABLE IF NOT EXISTS Usuarios (usuario_id int PRIMARY KEY AUTO_INCREMENT, nome VARCHAR(50) NOT NULL, " \
"senha VARCHAR(20) NOT NULL, email VARCHAR(50) NOT NULL)")

my_cursor.execute("CREATE TABLE IF NOT EXISTS Produtos (produto_id int PRIMARY KEY AUTO_INCREMENT, imagem VARCHAR(50), " \
 "nome_produto VARCHAR(100) NOT NULL, estoque VARCHAR(80) NOT NULL, descricao VARCHAR(300) NOT NULL," \
 " fornecedor VARCHAR(100) NOT NULL, criado_por VARCHAR(80) NOT NULL, criado_em date NOT NULL, " \
 "atualizado_em date NOT NULL)")

