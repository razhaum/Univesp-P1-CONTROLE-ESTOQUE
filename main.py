from flask import Flask , render_template, redirect, request, flash, session, jsonify
import os
import ast
import mysql.connector
from datetime import datetime  
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'VICTOR' 

#Configurações para conectar no banco de dados
db_config = {
    'host':'localhost',
    'user':'root',
    'passwd':'123',
    'auth_plugin':'mysql_native_password',
    'database':'gerenciamento_estoque'}


logado = False

@app.route('/')
def home():
    global logado
    logado = False
    return render_template('homepage.html')



@app.route('/cadastrarUsuario', methods=['GET','POST'])
def cadastrarUsuario():
    msg=''
    mydb = mysql.connector.connect(**db_config)
    my_cursor = mydb.cursor(buffered=True)
    if request.method =='POST':
            nome = request.form['nome']
            senha = request.form['senha']
            email = request.form['email']
            
            query_email = "SELECT * FROM Usuarios WHERE nome = %s"
            my_cursor.execute(query_email, (nome,))
            account = my_cursor.fetchone()

            if account:
                msg = 'Já existe uma conta com esse usuario!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Endereço de email inválido'
            elif not re.match(r'^[A-Za-z0-9]+$', nome):
                msg = 'Nome deve conter somente letras e números!'
            elif not nome or not senha or not email:
                msg = 'Preencha os campos obrigatórios'
            else:
                query_insert = "INSERT INTO Usuarios (nome, senha, email) VALUES (%s, %s, %s)"
                my_cursor.execute(query_insert, (nome, senha, email))
                mydb.commit() 
                msg = 'Registrado com sucesso!'
            
        
    # Buscar os usuários para exibir na página
    my_cursor.execute("SELECT * FROM Usuarios")
    usuarios = my_cursor.fetchall()

    my_cursor.close()
    mydb.close()
    return render_template('administrador.html', msg=msg, usuarios=usuarios)


@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        mydb = mysql.connector.connect(**db_config)
        cursor = mydb.cursor(buffered=True)
        nome = request.form["nome"]
        senha = request.form["senha"]

        # Checa se é admin
        if nome == 'adm' and senha == '000':
            cursor.close()
            mydb.close()
            return redirect('/cadastrarUsuario')

        # Checa usuários do banco
        cursor.execute('SELECT nome, senha FROM Usuarios')
        usuariosBD = cursor.fetchall()
        cursor.close()
        mydb.close()

        # Verifica se as credenciais batem
        for usuarioNome, usuarioSenha in usuariosBD:
            if nome == usuarioNome and senha == usuarioSenha:
                return redirect("/Produtos")

        # Se nenhum usuário bateu
        flash('USUARIO OU SENHA INVALIDO')
        return redirect("/")

    # GET: renderiza página de login
    return render_template("login.html")

    

#Rota pra excluir usuário
@app.route('/excluirUsuario',methods=['POST'])
def excluirUsuario():
    usuarioID = request.form.get('usuarioPexcluir')
    
    mydb = mysql.connector.connect(**db_config)
    my_cursor = mydb.cursor()
    my_cursor.execute("DELETE FROM Usuarios WHERE usuario_id = %s", (usuarioID,))
    mydb.commit()
    my_cursor.close()
    mydb.close()
    
    flash('Usuário excluído com sucesso!')
    return redirect('/cadastrarUsuario')


#Rota para adicionar produto
@app.route('/adicionarProduto', methods=['GET','POST'])
def adicionarProduto():
    msg=''
    if request.method =='POST':
            imagem = request.form['productImage']
            nome_produto = request.form['productName']
            estoque = str(request.form['productStock'])
            fornecedor = request.form['fornecedorName']
            descricao = request.form['productDescription']
            criado_por = request.form['criadoPor']
            criado_em = str(request.form['criadoEm'])
            atualizado_em = str(request.form['atualizadoEm'])
            nome_usuario = request.form.get('usuarioPexcluir')
  
            
            mydb = mysql.connector.connect(**db_config)
            my_cursor = mydb.cursor(buffered=True)
            query_produto = "SELECT * FROM Produtos WHERE nome_produto = %s AND fornecedor =%s"
            my_cursor.execute(query_produto, (nome_produto,fornecedor))
            produto_cadastrado = my_cursor.fetchone()

            if produto_cadastrado:
                msg = 'Produto já está cadastrado!'
            elif not nome_produto or not estoque or not fornecedor or not descricao or not criado_por or not criado_em or not atualizado_em:
               msg = 'Preencha os campos obrigatórios'
            else:
                query_insert = "INSERT INTO Produtos (imagem, nome_produto, estoque ,descricao, fornecedor, " \
                "criado_por,criado_em,atualizado_em) VALUES (%s, %s, %s,%s, %s, %s,%s,%s)"
                my_cursor.execute(query_insert, (imagem, nome_produto, estoque,descricao, fornecedor, 
                                                 criado_por,criado_em,atualizado_em))
                mydb.commit() 
                msg = 'Produto registrado com sucesso!'
                my_cursor.close()  
                mydb.close()
                return jsonify({'mensagem':msg})
    return render_template('dashboard.html', msg=msg)


#Rota para listar os produtos
@app.route('/Produtos')
def listar_produtos():
    mydb = mysql.connector.connect(**db_config)
    my_cursor = mydb.cursor(buffered=True)
    my_cursor.execute("SELECT produto_id, imagem, nome_produto, estoque, descricao," \
 " fornecedor, criado_por, criado_em, atualizado_em FROM Produtos")
    produtos = my_cursor.fetchall()
    print(produtos)
    my_cursor.close()

    return render_template('dashboard.html', produtos=produtos)



#Rota para deletar produto
@app.route('/deletarProduto', methods=['POST'])
def deletar_produto():
    produto_id = request.form['productId']

    mydb = mysql.connector.connect(**db_config)
    my_cursor = mydb.cursor(buffered=True)
    query_delete = "DELETE FROM Produtos WHERE produto_id = %s"
    my_cursor.execute(query_delete,(produto_id,))
    mydb.commit()
    msg = 'Produto deletado com sucesso!'
    my_cursor.close()
    mydb.close()
    return jsonify({'mensagem': msg})



#Rota para editar produto
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

    mydb = mysql.connector.connect(**db_config)
    my_cursor = mydb.cursor(buffered=True)
    query_update = "UPDATE Produtos set imagem = %s, nome_produto = %s, estoque = %s, " \
    "descricao = %s, fornecedor = %s, criado_por = %s, criado_em = %s, atualizado_em =%s" \
    "WHERE produto_id = %s"
    my_cursor.execute(query_update,(imagem, nome_produto, estoque, fornecedor, descricao, criado_por, 
                                    criado_em, atualizado_em, produto_id))
    mydb.commit()
    my_cursor.close()
    mydb.close()
    return jsonify({'mensagem': 'Produto atualizado com sucesso!'})



# Rota para logout
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    global logadol
    logado = False
    return redirect('/')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Pega a porta do Render, ou usa 5000 local
    app.run(host="0.0.0.0", port=port, debug=True)