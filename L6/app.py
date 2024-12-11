from flask import Flask, request, render_template, session, redirect, url_for, make_response

import sqlite3 
DATABASE = 'users.db'

app = Flask(__name__)
app.secret_key = 'SUPERSECRETA'

def get_connection():
    return sqlite3.connect(DATABASE)

def cria_tabela():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL     
                   )
        ''')
    conn.commit()
    conn.close()

cria_tabela()
    
@app.route('/cadastrar', methods=['POST', 'GET'])
def cadastrar():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] 

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                 INSERT INTO users(username, password)
                 VALUES (?, ?)''', (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))

        except sqlite3.IntegrityError:
            return render_template('cadastr.html', erro='Usuário já cadastrado.')
    
    return render_template('cadastrar.html')

    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
                SELECT * FROM users WHERE username = ? AND password  = ? ''', (username, password))
        usuario = cursor.fetchone()
        conn.close()
        if usuario:
            session['username'] = username 
            resposta = make_response(redirect(url_for('dashboard')))
            resposta.set_cookie('username', username, max_age= 60*60*24)
            return resposta 
        
        return render_template('login.html', erro='Usuário ou senha inválidos')
    
    if 'username' in session:
        return redirect(url_for('dashboard'))

    return render_template('login.html')        
      
@app.route('/dashboard')
def dashboard():
    #Verificar se o usuário está na sessão
    username = session.get('username')
    if not username:
        return redirect(url_for('login')) #Redirecionar para login se não estiver logado
    return render_template('dashboard.html', username=username)

@app.route('/logout', methods=['POST'])
def logout():
    #Remover usuário da sessão
    session.pop('username', None)
    #Remover o cookie 
    resposta = make_response(redirect(url_for('login')))
    resposta.set_cookie('username', '', max_age=0) #Excluir o cookie
    return resposta 
