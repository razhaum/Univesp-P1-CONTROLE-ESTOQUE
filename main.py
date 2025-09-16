from flask import Flask, render_template, redirect, request, flash, jsonify
import os
import re
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'VICTOR'

# Configurações para conectar no banco de dados PostgreSQL (Render)
db_config = {
    'host':'localhost',
    'user':'root',
    'passwd':'Lara296082**',
    'auth_plugin':'mysql_native_password',
    'database':'gerenciamento_estoque'}

def get_db_connection():
    conn = psycopg2.connect(**db_config, cursor_factory=RealDictCursor)
    return conn

logado = False

@app.route('/')
def home():
    global logado
    logado = False
    return render_template('homepage.html')

@app.route('/cadastrarUsuario', methods=['GET','POST'])
def cadastrarUsuario():
    msg = ''
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        email = request.form['email']

        cursor.execute("SELECT * FROM Usuarios WHERE nome = %s", (nome,))
        account = cursor.fetchone()

        if account:
            msg = 'Já existe uma conta com esse usuario!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Endereço de email inválido'
        elif not re.match(r'^[A-Za-z0-9]+$', nome):
            msg = 'Nome deve conter somente letras e números!'
        elif not nome or not senha or not email:
            msg = 'Preencha os campos obrigatórios'
        else:
            cursor.execute(
                "INSERT INTO Usuarios (nome, senha, email) VALUES (%s, %s, %s)",
                (nome, senha, email)
            )
            conn.commit()
            msg = 'Registrado com sucesso!'

    cursor.execute("SELECT * FROM Usuarios")
    usuarios = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('administrador.html', msg=msg, usuarios=usuarios)

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        nome = request.form["nome"]
        senha = request.form["senha"]

        # Checa se é admin
        if nome == 'adm' and senha == '000':
            cursor.close()
            conn.close()
            return redirect('/cadastrarUsuario')

        # Checa usuários do banco
        cursor.execute('SELECT nome, senha FROM Usuarios')
        usuariosBD = cursor.fetchall()
        cursor.close()
        conn.close()

        for usuario in usuariosBD:
            if nome == usuario['nome'] and senha == usuario['senha']:
                return redirect("/Produtos")

        flash('USUARIO OU SENHA INVALIDO')
        return redirect("/")

    return render_template("login.html")

@app.route('/excluirUsuario', methods=['POST'])
def excluirUsuario():
    usuarioID = request.form.get('usuarioPexcluir')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Usuarios WHERE usuario_id = %s", (usuarioID,))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Usuário excluído com sucesso!')
    return redirect('/cadastrarUsuario')

@app.route('/adicionarProduto', methods=['GET','POST'])
def adicionarProduto():
    msg = ''
    if request.method == 'POST':
        imagem = request.form['productImage']
        nome_produto = request.form['productName']
        estoque = str(request.form['productStock'])
        fornecedor = request.form['fornecedorName']
        descricao = request.form['productDescription']
        criado_por = request.form['criadoPor']
        criado_em = str(request.form['criadoEm'])
        atualizado_em = str(request.form['atualizadoEm'])

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Produtos WHERE nome_produto = %s AND fornecedor = %s", (nome_produto, fornecedor))
        produto_cadastrado = cursor.fetchone()

        if produto_cadastrado:
            msg = 'Produto já está cadastrado!'
        elif not nome_produto or not estoque or not fornecedor or not descricao or not criado_por or not criado_em or not atualizado_em:
            msg = 'Preencha os campos obrigatórios'
        else:
            cursor.execute(
                "INSERT INTO Produtos (imagem, nome_produto, estoque, descricao, fornecedor, criado_por, criado_em, atualizado_em) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (imagem, nome_produto, estoque, descricao, fornecedor, criado_por, criado_em, atualizado_em)
            )
            conn.commit()
            msg = 'Produto registrado com sucesso!'

        cursor.close()
        conn.close()
        return jsonify({'mensagem': msg})

    return render_template('dashboard.html', msg=msg)

@app.route('/Produtos')
def listar_produtos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT produto_id, imagem, nome_produto, estoque, descricao, fornecedor, criado_por, criado_em, atualizado_em FROM Produtos")
    produtos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('dashboard.html', produtos=produtos)

@app.route('/deletarProduto', methods=['POST'])
def deletar_produto():
    produto_id = request.form['productId']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Produtos WHERE produto_id = %s", (produto_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensagem': 'Produto deletado com sucesso!'})

@app.route('/editarProduto', methods=['POST'])
def editar_produto():
    produto_id = request.form['productId']
    imagem = request.form['productImage']
    nome_produto = request.form['productName']
    estoque = str(request.form['productStock'])
    fornecedor = request.form['fornecedorName']
    descricao = request.form['productDescription']
    criado_por = request.form['criadoPor']
    criado_em = request.form['criadoEm']
    atualizado_em = request.form['atualizadoEm']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Produtos SET imagem = %s, nome_produto = %s, estoque = %s, descricao = %s, fornecedor = %s, criado_por = %s, criado_em = %s, atualizado_em = %s "
        "WHERE produto_id = %s",
        (imagem, nome_produto, estoque, descricao, fornecedor, criado_por, criado_em, atualizado_em, produto_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensagem': 'Produto atualizado com sucesso!'})

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    global logado
    logado = False
    return redirect('/')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
