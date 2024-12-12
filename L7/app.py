from flask import Flask, request, render_template, session, redirect, url_for, make_response

app = Flask(__name__)
app.secret_key = 'SUPERSECRETA'

usuarios_registrados = []
user_usuario = []
user_adm =[]


@app.route('/cadastro', methods=['GET','POST'])
def cadastro():
    if request.method  == 'POST':
        username = request.form['username']
        password = request.form['password']
        nome = request.form['nome']
        funcao = request.form['funcao']

        user_encontrado = False
        #verificar se o user já existe
        for usuario in usuarios_registrados:
              if usuario['username'] == username:
                user_encontrado = True 
                return render_template('cadastro.html', erro='Usuário já cadastrado')
                
            
        # Adicionar novos users
        if not user_encontrado:
            usuarios_registrados.append({'username':username, 'password': password, 'nome': nome, 'funcao': funcao})

            if funcao == "ADM":
                user_adm.append({'username':username, 'password': password, 'nome': nome, 'funcao': funcao})

            elif funcao == "USER":
                user_adm.append({'username':username, 'password': password, 'nome': nome, 'funcao': funcao})

            return redirect(url_for('login'))
        
        return render_template('cadastro.html', erro='Nome de usuário já existente!')
    
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #Validar credenciais
        for usuario in usuarios_registrados:
            if usuario ['username'] == username and usuario['password'] == password:

                session['username'] = username
                resposta = make_response(redirect(url_for('dashboard')))
                resposta.set_cookie('username', username, max_age=60*60*24)
                return resposta
        return render_template('login.html', erro='Usuário ou senha inválidos.')
    
    if 'username' in session:
        return redirect(url_for('dashboard')) 
    return render_template('login.html')

@app.route('/usuarios')
def listar_usuarios():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    for usuario in usuarios_registrados:
        if usuario['username'] == username:
            funcao = usuario['funcao']

    if funcao == 'ADM':
        return render_template('usuarios.html', usuarios=user_adm)
    elif funcao == 'USER':
        return render_template('usuarios.html', usuarios=user_usuario)
        
 """
      # ... (código anterior)

def filtrar_usuarios(usuarios, query):
    return [usuario for usuario in usuarios if query.lower() in usuario['nome'].lower() or query.lower() in usuario['username'].lower()]

@app.route('/usuarios')
def listar_usuarios():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    for usuario in usuarios_registrados:
        if usuario['username'] == username:
            funcao = usuario['funcao']
            break

    query = request.args.get('query', '')
    usuarios_filtrados = filtrar_usuarios(usuarios_registrados, query)

    if funcao == 'ADM':
        return render_template('usuarios.html', usuarios=usuarios_filtrados)
    elif funcao == 'USER':
        # Filtrar apenas os usuários comuns
        usuarios_filtrados = [usuario for usuario in usuarios_filtrados if usuario['funcao'] == 'USER']
        return render_template('usuarios.html', usuarios=usuarios_filtrados)
 """

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
