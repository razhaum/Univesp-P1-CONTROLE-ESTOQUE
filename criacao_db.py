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
my_cursor.execute("CREATE TABLE IF NOT EXISTS Usuarios (usuario_id int PRIMARY KEY AUTO_INCREMENT, nome VARCHAR(50) NOT NULL, senha VARCHAR(20) NOT NULL, email VARCHAR(50) NOT NULL)")
for db in my_cursor:
    print(db)
