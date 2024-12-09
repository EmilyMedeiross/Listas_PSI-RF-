from flask import Flask, request, render_template, session, redirect, url_for, make_response

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chavesecreta'

@app.route('/sessao', methods=['GET', 'POST'])
def iniciar_sessao():
    if request.method == 'POST':

        session['nome'] = request.form['nome']
        session['idade'] = request.form['idade']

        return redirect(url_for('iniciar_sessao'))
    nome = session.get('nome')
    idade = session.get('idade')
    
    return render_template('sessao.html', nome=nome, idade=idade)

@app.route('/limpar_sessao')
def limpar_sessao():

    session.pop('nome', None)
    session.pop('idade', None)
    return redirect(url_for('iniciar_sessao'))

@app.route('/cookie', methods=['GET', 'POST'])
def definir_cookie():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']

        resposta  = make_response(redirect(url_for('definir_cookie')))

        resposta.set_cookie('nome', nome, max_age=60*60*24)

        resposta.set_cookie('idade', idade, make_age=60*60*24)

        return resposta
    
    nome = request.cookie.get('nome')
    idade = request.cookie.get('idade')
    return render_template('cookie.html', nome=nome, idade=idade)