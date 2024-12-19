from models import *
from time import sleep
from datetime import datetime
from flask import Blueprint, request, redirect, render_template, session, url_for, flash


doctor_bp = Blueprint('doctor', __name__)


# rota para client/main.html, endpoint (oq aparece no navegador) "/"
@doctor_bp.route('/home', methods=["GET", "POST"], endpoint="/home")
def main():
    if request.method == "GET":
        return render_template('admin/doctor/main.html')
        

# rota para client/cadastro.html, endpoint (oq aparece no navegador) "/cadastro"
@doctor_bp.route('/cadastro', methods=["GET", "POST"], endpoint="/cadastro")
def cadastroMedico():
        # se for get, página
        if request.method == "GET":
            return render_template('admin/doctor/cadastro.html')

        # se for post, cadastro
        if request.method == "POST":
            # salva dados do form - nome, data de nascimento, cpf, telefone, email e senha
            name = request.form["name"] 
            nasc = datetime.strptime(request.form["nasc"], "%Y-%m-%d").date()
            salario = request.form["salario"]
            cpf = request.form["cpf"]
            telefone = request.form["telefone"]
            crmv = request.form["crmv"]
            email = request.form["email"]
            dataContratacao = request.form["contratacao"]
            dataContratacao = datetime.strptime(request.form["contratacao"], "%Y-%m-%d").date()
            senha = ""

            # adicionando dados ao Modelo criado anteriormente
            medico = Medico(name, nasc, salario, cpf, telefone, crmv, email, dataContratacao, senha)

            # adicionando mudanças ao banco de dados 
            db.session.add(medico)
            db.session.commit()
            return render_template("admin/doctor/cadastro.html")


# rota para client/update.html, endpoint (oq aparece no navegador) "/atualizar"
@doctor_bp.route('/atualiza', methods=["GET", "POST"], endpoint="/atualiza")
def update():
    # se get, página
    if request.method == "GET":
        medicos = getAllMedicos()
        return render_template("admin/doctor/updateCenter.html", medicos=medicos)
    


# rota para client/update.html, endpoint (oq aparece no navegador) "/atualizar"
@doctor_bp.route('/atualizar', methods=["GET", "POST"], endpoint="/atualizar")
def update():
    # se get, página
    if request.method == "GET":
        id = int(request.args.get('id'))
        print(id)
        medico = Medico.query.filter_by(id=id).first()
        return render_template("admin/doctor/update.html", medico=medico)
    # se post, update
    elif request.method == "POST":
        cpf = request.form["cpf"]
        print(f'POST CPF {cpf}')
        medico = Medico.query.filter_by(cpf=cpf).first()
        print(f"POST MEDICO: {medico}")
        id = medico.id
        print(f"POST ID: {id}")
        res = updateById(id)
        print(f"RES: {res}")
        if res == 0:
            return render_template("admin/doctor/update.html", medico=medico)
        else:

            return render_template("admin/doctor/update.html", medico= medico)
    

@doctor_bp.route('/deletar', methods=["GET", "POST"], endpoint="/deletar")
def deleteMedico():
    if request.method == "GET":
        medicos = Medico.query.all()
        return render_template("admin/doctor/delete.html", medicos=medicos)
    try:
        deleteById(request.form['id'])
        medicos = Medico.query.all()
        return render_template("admin/doctor/delete.html", medicos=medicos) 
    except Exception as e:
        print(e)
        return str(e)
    

# rota para client/data.html, endpoint (oq aparece no navegador) "/data"
# basicamente, dá um get em todos os Medicoes cadastrados
# não existe como (o Medico) chegar nessa rota via interface 
@doctor_bp.route('/data', methods=["GET"], endpoint="/data")
def getAllMedicos():
    medicos = getAllMedicos()
    return render_template('admin/doctor/getAll.html', medicos = medicos)


#
# FUNÇÕES DO CRUD E FUNCIONALIDADE (LOGIN)
#

# create Medico | FEITO
def createMedico():
    try:
        # salvando dados do forms
        nome = request.form["nome"]
        nasc = datetime.strptime(request.form["nasc"], "%Y-%m-%d").date()
        salario = request.form["salario"]
        cpf = request.form["cpf"]
        telefone = request.form["telefone"]
        crmv = request.form["crmv"]
        email = request.form["email"]
        dataContratacao = request.form["contratacao"]
        senha = ""
        
        # instanciando o modelo criado com os dados do usuário
        medico = Medico(nome, nasc, salario, cpf, telefone, crmv, email, dataContratacao, senha)
        
        # adicionando mudanças ao banco de dados
        db.session.add(medico)

        # commitando as alterações
        db.session.commit()


        return 0

    except:

        # status code, 1, se algo der errado (o que? não sabemos) 
        return render_template("client/cadastro.html")


# read all | FINALIZADA
def getAllMedicos():
    try:
        Medicos = Medico.query.all()
        return Medicos

    except:

        # status code, 2, se algo der errado (o que? não sabemos) 
        return 2


# update by id
def updateById(idMedico):
    
    try:
        medico = Medico.query.filter_by(id=idMedico).first()
        
        medico.nome = request.form["nome"]
        medico.nasc = datetime.strptime(request.form["nasc"], "%Y-%m-%d").date()
        medico.salario = request.form["salario"]
        medico.cpf = request.form["cpf"]
        medico.telefone = request.form["telefone"]
        medico.crmv = request.form["crmv"]
        medico.email = request.form["email"]
        medico.dataContratacao = datetime.strptime(request.form["contratacao"], "%Y-%m-%d").date()
        medico.senha = ""

        db.session.commit()
        
        return 0
    
    except Exception as e:
        print(f"Exception: {e}")
        return 4

# delete by id
def deleteById(id):
    
    try:
        medico = Medico.query.filter_by(id=id).first()
        db.session.delete(medico)
        db.session.commit()
    
        return 0

    except:

        return 5
    
