from flask import Flask , render_template, redirect, request, flash, url_for, make_response, jsonify
import json
import mysql.connector
import re

#Conecta o banco de dados
mydb = mysql.connector.connect(
    host ="localhost",
    user = "root",
    passwd = "110719",
    auth_plugin = "mysql_native_password",
    database = "gerenciamento_estoque")

#my_cursor = mydb.cursor(buffered=True)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'VICTOR' 
app.config['JSON_SORT_KEYS'] = False # envia os dados como estão no banco de dados

@app.route('/')
def home():
    return render_template('homepage.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/registro', methods=['GET','POST'])
def registro():
    msg = ''
    if request.method =='POST' and 'nome' in request.form and 'senha' in request.form and 'email' in request.form:
        nome = request.form['nome'].strip()
        senha = request.form['senha'].strip()
        email = request.form['email'].strip()

        my_cursor = mydb.cursor(buffered=True)
        query_email = "SELECT * FROM Usuarios WHERE email = %s"
        my_cursor.execute(query_email, (email,))
        account = my_cursor.fetchone()

        if account:
            msg = 'Já existe uma conta com esse email!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Endereço de email inválido'
        elif not re.match(r'^[A-Za-z0-9]+$', nome):
            msg = 'Nome deve conter somente letras e números!'
        elif not nome or not senha or not email:
            msg = 'Preencha os campos obrigatórios'
        else:
            query_insert = "INSERT INTO Usuarios (nome, senha, email) VALUES (%s, %s, %s)"
            my_cursor.execute(query_insert, (nome, senha, email))
            mydb.commit()  # <<< Use this, not mysql.connection.commit()
            msg = 'Registrado com sucesso!'
    return render_template('registro.html', msg=msg)


#@app.route('/login', methods=['POST'])
#def login():  
#    nome = request.form.get('nome')
#    senha = request.form.get('senha')
# abrir o arquivo json e transformar em lista python
#    with open('usuarios.json') as usuariosTemp:
#        usuarios = json.load(usuariosTemp)
#        cont = 0

#        for usuario in usuarios:
#            cont +=1
#            if nome == 'adm' and senha =='000':
#                return render_template("administrador.html")
#            if usuario['nome'] == nome and usuario['senha'] == senha:
#                return render_template("dashboard.html")
#
#            if cont >= len(usuarios):
#                flash('USUARIO INVALIDO')
#                return redirect("/")
    

if __name__ in "__main__":
    app.run(debug=True)