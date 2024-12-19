import os
from models import *
from datetime import datetime
from flask_session import Session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import controllers.petController as petController
import controllers.adminController as adminController
import controllers.tutorController as tutorController
import controllers.medicoController as doctorController
import controllers.productController as productController
import controllers.consultaController as consultaController
from flask import Flask, render_template, request, redirect, session


# Configurações gerais da aplicação e db
app = Flask(__name__) # criação da aplicação Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vitapet.db' # caminho do db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # não salvar um histórico modificações do db
app.secret_key = os.urandom(24) # secret key random


# configurações de Session
app.config['SESSION_TYPE'] = 'filesystem' # salva o arquivo de session na máquina 
app.config['SESSION_PERMANENT'] = True # a session não tem prazo de validade
Session(app) # linka os cookies do usuário com a aplicação Flask


# iniciando o banco de dados (linkando à aplicação)
db.init_app(app)
# "ativando" a opção de migrations para possíveis alterações no db
migrate = Migrate(app, db)


# registrando o Blueprint (responsável pelas rotas) do usuário com prefixo "/tutor"
app.register_blueprint(petController.pet_bp, url_prefix="/pet")
app.register_blueprint(adminController.admin_bp, url_prefix="/admin")
app.register_blueprint(tutorController.tutor_bp, url_prefix="/tutor")
app.register_blueprint(doctorController.doctor_bp, url_prefix="/doctor")
app.register_blueprint(productController.product_bp, url_prefix="/product")
app.register_blueprint(consultaController.consulta_bp, url_prefix="/consulta")

# criando todas as tabelas antes de qualquer requisição
@app.before_request
def create_table():
    db.create_all()


# rota para index.html - homepage do petshop/projeto
@app.route('/')
def home():
    return render_template('index.html')


@app.route("/home")
def homeRoute():
    return render_template('index.html')


# rodar a aplicação na porta 5000 com debug ativado
# pq o debug tá ativado? para q possamos fzr alterações sem precisar matar o server
if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
