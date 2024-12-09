from flask import Flask
from flask import request, render_template


app = Flask(__name__)

@app.route('/')
def home():
    return "Bem-vindo ao Flask!"

@app.route('/sobre')
def sobre():
    return "Está página é sobre Flask"

@app.route('/saudacao/<nome>')
def saudacao(nome):
    return f"Olá, {nome}! Bem-vindo ao Flask!"
    
@app.route('/contato/<tel>', methods=['POST', 'GET'])
def contato(tel):
    return f"Olá,! seu telefone é: {tel}!"
    