from models import *
from time import sleep
from datetime import datetime
from flask import Blueprint, request, redirect, render_template, session, url_for, flash


consulta_bp = Blueprint('consulta', __name__)


@consulta_bp.route('/home', methods=["GET"], endpoint="/home")
def home():
    return render_template("client/appointment/main.html")


@consulta_bp.route('/marcar', methods=["GET", "POST"], endpoint="/marcar")
def marcar():
    if request.method == "GET":
        return render_template("client/appointment/marcar.html")
    if request.method == "POST":
        medico = request.form['medico']
        pet = request.form['pet']
        data = datetime.strptime(request.form["data"], "%Y-%m-%d").date()
        preco = request.form['preco']

        consulta = Consulta(medico, pet, preco, data)

        db.session.add(consulta)
        db.session.commit()

        return 'consulta marcada!'
    

@consulta_bp.route('/marcadas', methods=["GET"], endpoint="/marcadas")
def marcadas():
    if request.method == "GET":
        consultas = Consulta.query.all()
        return render_template("client/appointment/getAll.html", consultas=consultas)


@consulta_bp.route('/remarca', methods=["GET"], endpoint="/remarca")
def remarca():
    if request.method == "GET":
        consultas = Consulta.query.filter_by()
        return render_template("client/appointment/updateCenter.html", consultas=consultas)


@consulta_bp.route('/remarcar', methods=["GET", "POST"], endpoint="/remarcar")
def remarcar():
    id = int(request.args.get('id'))
    
    consulta = Consulta.query.filter_by(id=id).first()
    if request.method == "GET":
        return render_template("client/appointment/update.html", consulta=consulta)
    if request.method == "POST":
        
        consulta.id_medico = request.form['medico']
        consulta.id_animal = request.form['animal']
        consulta.dataConsulta =  datetime.strptime(request.form["data"], "%Y-%m-%d").date()
        consulta.valor = request.form['valor']
        
        db.session.commit()
        return "remarcado com sucesso!"


@consulta_bp.route('/cancelar', methods=["GET", "POST"], endpoint="/cancelar")
def cancelar():
    if request.method == "GET":
        consultas = Consulta.query.all()
        return render_template("client/appointment/delete.html", consultas = consultas)
    if request.method == "POST":
        id = request.form['id']
        consulta = Consulta.query.filter_by(id=id).first()
        db.session.delete(consulta)
        db.session.commit()

        return "cancelada com sucesso!"