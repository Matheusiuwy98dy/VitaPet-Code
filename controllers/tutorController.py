from models import *
from time import sleep
from datetime import datetime
from flask import Blueprint, request, redirect, render_template, session, url_for, flash


tutor_bp = Blueprint('tutor', __name__)
    

# rota para client/main.html, endpoint (oq aparece no navegador) "/"
@tutor_bp.route('/home', methods=["GET", "POST"], endpoint="/home")
def main():
    # se for um get, retorna a página client/main.html
    if request.method == "GET":
        return render_template('client/main.html')
    
    # se for um post, verifica o login
    if request.method == "POST":

        # salva o email passado no form
        emailCadastrado = request.form["email"]
        # salva a senha
        senha = request.form["senha"]
        # chama a função de login e salva a resposta na variável "res"
        res = login(emailCadastrado, senha)
        print(res)
        # se a resposta for 0, significa q deu tudo certo
        if res == 0:
            # busca o tutor pelo email fornecido (a senha foi verifcada na função login)
            tutor = Tutor.query.filter_by(email=emailCadastrado).first()
            # salva os dados na session
            session["id"] = tutor.id
            session["nome"] = tutor.nome
            session["nasc"] = tutor.nasc
            session["cpf"] = tutor.cpf
            session["telefone"] = tutor.telefone
            session["email"] = tutor.email
            session["senha"] = tutor.senha
            print(session)
            # retorna a página
            return render_template('client/main.html', tutor=session)

        # se a reposta for 6 significa q a senha está errada
        elif res == 6:
            return render_template('client/login.html')
            # fazer error na interface
    
        # 7 é tutor não cadastrado
        elif res == 7:
            return render_template('client/login.html')
        
        # não tem como esse erro existir, mas coloquei para caso
        # exista e eu não tenha percebido
        else:
            return render_template('client/login.html') # impossível chegar aqui (eu acho)
        


# rota para client/login.html, endpoint (oq aparece no navegador) "/login"
@tutor_bp.route('/login', methods=["GET"], endpoint="/login")
def loginPage():
    # retorna a página client/login.html
    return render_template('client/login.html')



# rota para client/cadastro.html, endpoint (oq aparece no navegador) "/cadastro"
@tutor_bp.route('/cadastro', methods=["GET", "POST"], endpoint="/cadastro")
def cadastroTutor():
        # se for get, página
        if request.method == "GET":
            return render_template('client/cadastro.html')

        # se for post, cadastro
        if request.method == "POST":
            # salva dados do form - nome, data de nascimento, cpf, telefone, email e senha
            name = request.form["name"] 
            nasc = datetime.strptime(request.form["nasc"], "%Y-%m-%d").date()
            cpf = request.form["cpf"]
            telefone = request.form["telefone"]
            email = request.form["email"]
            senha = request.form["senha"]

            # adicionando dados ao Modelo criado anteriormente
            tutor = Tutor(name, nasc, cpf, telefone, email, senha)

            # adicionando mudanças ao banco de dados
            db.session.add(tutor)
            db.session.commit()

            # redireciona à pagina de login (achei melhor doq mandar pra main pq já testa o login tbm)
            return redirect(url_for('tutor./login'))



# rota para client/update.html, endpoint (oq aparece no navegador) "/atualizar"
@tutor_bp.route('/atualizar', methods=["GET", "POST"], endpoint="/atualizar")
def update():
    # se get, página
    if request.method == "GET":
        return render_template("client/update.html")
    # se post, update
    elif request.method == "POST":
        id = session['id']
        print(f"ID: {id}")
        res = updateById(id)
        print(f"RES: {res}")
        return render_template("client/update.html")
    


@tutor_bp.route('/deletar', methods=["POST"], endpoint="/deletar")
def deleteTutor():
    try:
        deleteById(session["id"])
        sleep(3)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)
        return str(e)
    

@tutor_bp.route("/logout", methods=["GET"], endpoint="/logout")
def logout():
    session.clear()
    return redirect(url_for('tutor./login'))
# rota para client/data.html, endpoint (oq aparece no navegador) "/data"
# basicamente, dá um get em todos os tutores cadastrados
# não existe como (o tutor) chegar nessa rota via interface 
@tutor_bp.route('/data')
def getAllTutires():
    tutores = Tutor.query.all()
    return render_template('client/getAll.html', tutores = tutores)


#
# FUNÇÕES DO CRUD E FUNCIONALIDADE (LOGIN)
#

# create Tutor | FEITO
def createTutor():
    try:
        # salvando dados do forms
        name = request.form["name"] 
        nasc = datetime.strptime(request.form["nasc"], "%Y-%m-%d").date()
        cpf = request.form["cpf"]
        telefone = request.form["telefone"]
        email = request.form["email"]
        
        # instanciando o modelo criado com os dados do usuário
        tutor = Tutor(name, nasc, cpf, telefone, email)
        tutor.senha= request.form["senha"]

        # adicionando mudanças ao banco de dados
        db.session.add(tutor)

        # commitando as alterações
        db.session.commit()


        return 0

    except:

        # status code, 1, se algo der errado (o que? não sabemos) 
        return render_template("client/cadastro.html")


# read all | FINALIZADA
def getAllTutores():
    try:
        Tutores = Tutor.query.all()
        return Tutores

    except:

        # status code, 2, se algo der errado (o que? não sabemos) 
        return 2


"""
APARENTEMENTE ESSA FUNÇÃO É INÚTL PORQUE A SESSION
FACILITA A PASSAGEM DE DADOS ENTRE PÁGINAS DOS APP 


# read by id | só vou testar qnd tiver fzr bglh de adm
def getTutorByEmail(emailCadastrado, OnlyId=False):
    try:
        tutor = Tutor.query.filter_by(email=emailCadastrado).first()
        
        if OnlyId:
            return tutor.id
        else:
            return tutor
    
    except:

        # status code, 3, se algo der errado (o que? não sabemos) 
        return 3
    """

# update by id
def updateById(idTutor):
    
    try:
        tutor = Tutor.query.filter_by(id=idTutor).first()
        
        tutor.nome = request.form["name"]
        tutor.nasc = datetime.strptime(request.form["nasc"], "%Y-%m-%d").date()
        tutor.cpf = request.form["cpf"]
        tutor.telefone = request.form["telefone"]
        tutor.email = request.form["email"]
        tutor.senha = request.form["senha"]
            
        db.session.commit()

        session["nome"] = tutor.nome  
        session["nasc"] = tutor.nasc 
        session["cpf"] = tutor.cpf 
        session["telefone"] = tutor.telefone 
        session["email"] = tutor.email 
        session["senha"] = tutor.senha
        
        return 0
    
    except:
        return 4

# delete by id
def deleteById(id):
    
    try:
        tutor = Tutor.query.filter_by(id=id).first()
        print(tutor)
        db.session.delete(tutor)
        db.session.commit()
    
        return 0

    except:

        return 5
    

# login | FINALIZADA
def login(emailCadastrado, senha):
    try:
        tutor = Tutor.query.filter_by(email=emailCadastrado).one_or_none()
        
        if tutor is not None:
        
            isPasswordCorrect = (tutor.senha == senha)
        
            if isPasswordCorrect:        
                return 0

            else:
                isPasswordCorrect = False
                return 6
        
        else:
            return 7
        
    except Exception as e:
        print(f"Error: {e}")
        return 8
