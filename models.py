from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# classe médico
class Medico(db.Model):
    # nome da tabela
    __tablename__ = "Medico"
    # id do médico - inteiro, primary key, autoincrement 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # nome do médico - string/varchar de 40 caracteres, não nulo/not null 
    nome = db.Column(db.String(40), nullable=False)
    # nascimento do médico - tipo Date, not null/não nulo
    nasc = db.Column(db.Date, nullable=False)
    # salário do médico - tipo Float, not null
    salario = db.Column(db.Float, nullable=False)
    # cpf do médico - string/varchar de 11 caracteres, unique key (chave única)
    cpf = db.Column(db.String(11), unique=True)
    # telefone do médico - string de 11 caracteres, unique key
    telefone = db.Column(db.String(11), unique=True)
    # crmv do médico - string de 4 caracteres, unique key
    crmv = db.Column(db.String(4), unique=True)
    # email do médico - string de 255 caracteres, unique key
    email = db.Column(db.String(255), unique=True)
    # data de contratação do médico, Date, not null
    dataContratacao = db.Column(db.Date, nullable=False)
    # senha para login - varchar(20), not null
    senha = db.Column(db.String(20), nullable=False)

    def __init__(self, nome, nasc, salario, cpf, telefone, crmv, email, dataContratacao, senha):
        self.nome = nome
        self.nasc = nasc
        self.salario = salario
        self.cpf = cpf
        self.telefone = telefone
        self.crmv = crmv
        self.email = email
        self.dataContratacao = dataContratacao
        self.senha = senha

# Classe tutor
class Tutor(db.Model):
    # nome da tabela
    __tablename__ = "Tutor"
    # id do tutor - inteiro, primary key, autoincrement 
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    # nome do tutor - string de 40 caracteres, not null
    nome = db.Column(db.String(40), nullable=False)
    # nascimento do tutor - tipo Date, not null/não nulo
    nasc = db.Column(db.DateTime, nullable=False)
    # cpf do tutor - string/varchar de 11 caracteres, unique key (chave única)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    # telefone do tutor - string de 11 caracteres, unique key
    telefone = db.Column(db.String(11), unique=True, nullable=False)
    # email do tutor - string de 255 caracteres, unique key
    email = db.Column(db.String(255), unique=True, nullable=False)
    # senha para login - varchar(20), not null
    senha = db.Column(db.String(128), nullable=True)

    def __init__(self, nome, nasc, cpf, telefone, email, senha):
        self.nome = nome
        self.nasc = nasc
        self.cpf = cpf
        self.telefone = telefone
        self.email = email
        self.senha = senha

class Animal(db.Model):
    # nome da tabela
    __tablename__ = "Animal"
    # id do pet - inteiro, primary key, autoincrement 
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    # nome do pet - string de 40 caracteres, not null
    nome = db.Column(db.String(40), nullable=False)
    # nascimento do pet - tipo Date, not null/não nulo
    nasc = db.Column(db.DateTime, nullable=False)
    # tipo do pet - string de 40 caracteres, not null | ex: cachorro, gato, pássaro
    tipo = db.Column(db.String(40), nullable=False)
    # raça do pet - string de 40 caracteres, not null | ex: rottweiler, Siamês, bem-te-vi
    raca = db.Column(db.String(40), nullable=False)
    # altura do pet - tipo float, pode ser null pq pode ser medido na hr da consulta | ex: 30cm 
    altura = db.Column(db.Float)
    # id do dono do pet - int, not null, Foreign Key (FK)
    id_tutor = db.Column(db.Integer, db.ForeignKey('Tutor.id'), nullable=False)
    
    def __init__(self, nome, nasc, tipo, raca, altura, id_tutor):
        self.nome = nome
        self.nasc = nasc
        self.tipo = tipo
        self.raca = raca
        self.altura = altura
        self.id_tutor = id_tutor

class Produto(db.Model):
    # nome da tabela
    __tablename__ = "Produto"
    # id do médico - inteiro, primary key, autoincrement 
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    # nome do produto
    nome = db.Column(db.String(255), nullable=False)
    # preço do produto
    preco = db.Column(db.Float, nullable=False)
    # quantidade disponível
    qtd_disponivel = db.Column(db.Integer, nullable=False)

    def __init__(self, nome, preco, qtd_disponivel):
        self.nome = nome
        self.preco = preco
        self.qtd_disponivel = qtd_disponivel
    
class Consulta(db.Model):
    # nome da tabela
    __tablename__ = "Consulta"
    # id do médico - inteiro, primary key, autoincrement 
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    # id do médico - inteiro, foreign key, autoincrement - referencia o id na tabela médico 
    id_medico = db.Column(db.Integer, db.ForeignKey('Medico.id'), nullable=False)
    # id do pet - inteiro, foreign key, autoincrement - referencia o id na tabela animal
    id_animal = db.Column(db.Integer, db.ForeignKey('Animal.id'), nullable=False)
    # valor pago pela consulta - float, not null 
    valor = db.Column(db.Float, nullable=False)
    # data da consulta - date, not null
    dataConsulta = db.Column(db.Date, nullable=False)

    def __init__(self, id_medico, id_animal, valor, dataConsulta):
        self.id_medico = id_medico
        self.id_animal = id_animal
        self.valor = valor
        self.dataConsulta = dataConsulta
