from flask import Flask, request, render_template

app = Flask (__name__)

@app.route('/')
def home():
    return "Página Inicial"

@app.route('/formulario', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        mensagem = request.form.get('mensagem')

        return f'Obrigada pelo feedback, {nome}!\nEndereço de email: {email}.\nMensagem recebida:\n{mensagem}'

    
        # comentario = request.form.get
        # ('comentario')
        # return f'Obrigado pelo seu feedback, {nome}! Comentário recebido: {comentario}'
    
    return "Bem-vindo ao formulário. Por favor, envie seu email." + render_template('formulario.html')

