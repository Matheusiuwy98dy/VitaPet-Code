from models import *
from time import sleep
from datetime import datetime
from flask import Blueprint, request, redirect, render_template, session, url_for


pet_bp = Blueprint('pet', __name__)


# rota p main
@pet_bp.route("/", methods=["GET"], endpoint="/")
def main():
    return render_template("client/pet/main.html")


# rota para client/cadastro.html, endpoint (oq aparece no navegador) "/cadastro"
@pet_bp.route('/cadastro', methods=["GET", "POST"], endpoint="/cadastro")
def cadastroTutor():
        # se for get, página
        if request.method == "GET":
            return render_template('client/pet/cadastro.html')

        # se for post, cadastro
        if request.method == "POST":
            # salva dados do form - nome, data de nascimento, cpf, telefone, email e senha
            name = request.form["name"] 
            nasc = datetime.strptime(request.form["nasc"], "%Y-%m-%d").date()
            tipo = request.form["tipo"]
            raca = request.form["raca"]
            altura = request.form["altura"]
            id_tutor = session["id"]

            # adicionando dados ao Modelo criado anteriormente
            pet = Animal(name, nasc, tipo, raca, altura, id_tutor)

            # adicionando mudanças ao banco de dados
            db.session.add(pet)
            db.session.commit()

            # redireciona à pagina de login (achei melhor doq mandar pra main pq já testa o login tbm)
            return render_template('client/pet/cadastro.html')


# rota para client/update.html, endpoint (oq aparece no navegador) "/atualizar"
@pet_bp.route('/atualiza', methods=["GET"], endpoint="/atualizar")
def updateCenter():
    # se get, página
    petsDoTutor = Animal.query.filter_by(id_tutor=session['id']).all()
    print(petsDoTutor)
    print(session["id"])
    if request.method == "GET":
        return render_template("client/pet/updateCenter.html", pets=petsDoTutor)
    # se post, update


@pet_bp.route('/atualizarPet', methods=["GET", "POST"], endpoint='/atualizarPet')
def update():
    
    if request.method == "GET":
        pet_id = int(request.args.get('pet_id'))
        print(f"PET ID: {pet_id}")
        pet = Animal.query.filter_by(id=pet_id).first()
        print(pet)
        return render_template('client/pet/update.html', pet=pet)
    
    if request.method == "POST":
        pet_id = request.args.get('id')
        print(f"PET ID POST: {pet_id}")
        res = updateById(pet_id)
        print(res)
        pet = Animal.query.filter_by(id=pet_id).first()
        return render_template("client/pet/update.html", pet=pet)


@pet_bp.route('/deletar', methods=["GET", "POST"], endpoint="/deletar")
def deleteTutor():
        
    petsDoTutor = Animal.query.filter_by(id_tutor=session['id'])
    if request.method == "GET":
        return render_template("client/pet/deleteCenter.html", pets = petsDoTutor)
    
    if request.method == "POST":
        pet_id = request.form["id"]
        print(f"PET ID POST: {pet_id}")
        res = deleteById(pet_id)
        print(res)
        return render_template("client/pet/deleteCenter.html")
    

# rota para client/data.html, endpoint (oq aparece no navegador) "/data"
# basicamente, dá um get em todos os tutores cadastrados
# não existe como (o tutor) chegar nessa rota via interface 
@pet_bp.route('/data')
def getAllTutires():
    pets = Animal.query.all()
    return render_template('client/pet/getAll.html', pets = pets)





# create Pet | FINALIZADA
def createPet():
    try:
        # salvando dados do forms
        nome = request.form["name"] 
        nasc = datetime.strptime(request.form["nasc"], "%Y-%m-%d").date()
        tipo = request.form["tipo"]
        raca = request.form["raca"]
        altura = request.form["altura"]
        id_tutor = session["id"]
        
        # instanciando o modelo criado com os dados do usuário
        pet = Animal(nome, nasc, tipo, raca, altura, id_tutor)

        # adicionando mudanças ao banco de dados
        db.session.add(pet)

        # commitando as alterações
        db.session.commit()


        return 0

    except:

        # status code, 1, se algo der errado (o que? não sabemos) 
        return render_template("client/cadastro.html")


# read all | FINALIZADA
def getAllPet():
    try:
        Pets = Animal.query.all()
        return Pets

    except:

        # status code, 2, se algo der errado (o que? não sabemos) 
        return 2

def getPetsByTutorId(id):
    try:
        pets = Animal.query.filter_by(id_tutor=id)
        print(pets)
        return pets
    except:
        return 10
# update by id
def updateById(id):
    
    try:
        pet = Animal.query.filter_by(id=id).first()
        
        pet.nome = request.form["name"]
        pet.nasc = datetime.strptime(request.form["nasc"], "%Y-%m-%d").date()
        pet.tipo = request.form["tipo"]
        pet.raca = request.form["raca"]
        pet.altura = request.form["altura"]
            
        db.session.commit()
        
        return 0
    
    except:
        return 4

# delete by id
def deleteById(id):
    
    try:
        pet = Animal.query.filter_by(id=id).first()
        print(pet)
        db.session.delete(pet)
        db.session.commit()
    
        return 0

    except:

        return 5
    
