import mysql.connector

mydb = mysql.connector.connect(
    host ="localhost",
    user = "root",
    passwd = "110719",
    auth_plugin = "mysql_native_password",
    database = "gerenciamento_estoque")

my_cursor = mydb.cursor()
my_cursor.execute("SELECT * FROM Usuarios")
for x in my_cursor:
    print(x)