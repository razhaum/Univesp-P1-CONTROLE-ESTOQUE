from flask import Flask , render_template, redirect, request, flash, url_for
from flask_sqlal'
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'VICTOR' 


@app.route('/')
def home():
    return render_template('homepage.html')


@app.route('/login')
def login_init():
    return render_template('login.html')


@app.route('/registro')
def registro():
    return render_template('registro.html')


@app.route('/login', methods=['POST'])
def login():  
    nome = request.form.get('nome')
    senha = request.form.get('senha')
# abrir o arquivo json e transformar em lista python
    with open('usuarios.json') as usuariosTemp:
        usuarios = json.load(usuariosTemp)
        cont = 0

        for usuario in usuarios:
            cont +=1
            if nome == 'adm' and senha =='000':
                return render_template("administrador.html")
            if usuario['nome'] == nome and usuario['senha'] == senha:
                return render_template("dashboard.html")

            if cont >= len(usuarios):
                flash('USUARIO INVALIDO')
                return redirect("/")
                 








if __name__ in "__main__":
    app.run(debug=True)