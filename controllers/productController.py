from models import *
from time import sleep
from datetime import datetime
from flask import Blueprint, request, redirect, render_template, session, url_for, flash


product_bp = Blueprint('produto', __name__)

@product_bp.route('/home', methods=["GET"], endpoint="/home")
def home():
    return render_template("admin/products/main.html")

@product_bp.route('/cadastro', methods=["GET", "POST"], endpoint="/cadastro")
def cadastro():
    if request.method == "GET":
        return render_template("admin/products/cadastro.html")
    if request.method == "POST":
        res = createProduto()
        if res == 0:
            return render_template("admin/products/cadastro.html")
        else:
            return render_template("admin/products/cadastro.html")


@product_bp.route('/data', methods=["GET"], endpoint="/data")
def getAll():
    produtos = Produto.query.all()
    return render_template('admin/products/getAll.html', produtos=produtos)


@product_bp.route('/atualiza', methods=["GET"], endpoint="/atualiza")
def atualiza():
    if request.method == "GET":
        produtos = Produto.query.all()
        return render_template('admin/products/updateCenter.html', produtos=produtos)

@product_bp.route('/atualizar', methods=["GET", "POST"], endpoint="/atualizar")
def atualizar():
    try:
        if request.method == "GET":
            id = int(request.args.get('id'))
            produto = Produto.query.filter_by(id=id).first()
            return render_template('admin/products/update.html', produto=produto)
        if request.method == "POST":
            id = request.form['id']
            produto = Produto.query.filter_by(id=id).first()
            
            produto.nome = request.form['nome']
            produto.preco = request.form['preco']
            produto.estoque = request.form['estoque']

            db.session.commit()

            return render_template('admin/products/update.html', produto=produto)
        
    except Exception as e:
        print(f"ERRO {e}")
        return render_template('admin/products/update.html')


@product_bp.route('/deletar', methods=["GET", "POST"], endpoint="/deletar")
def deletar():
    try:
        if request.method == "GET":
            produtos = Produto.query.all()
            return render_template('admin/products/delete.html', produtos=produtos)
        if request.method == "POST":
            id = int(request.form['id'])
            res = deleteById(id)
            print(f'RES: {res}')
            produtos = Produto.query.all()
            return render_template('admin/products/delete.html', produtos=produtos)
                  
    except Exception as e:
        print(f"ERROR: {e}")
        return render_template('admin/products/delete.html')

            
def createProduto():
    try:
        nome = request.form["name"]
        preco = request.form["preco"]
        estoque = request.form["estoque"]

        produto = Produto(nome, preco, estoque)

        db.session.add(produto)
        db.session.commit()

        return 0
    
    except Exception as e:
        print(f"error: {e}")
        return 5
    

def deleteById(id):
    try:
        produto = Produto.query.filter_by(id=id).first()
        
        db.session.delete(produto)
        db.session.commit()

        return 0
    
    except Exception as e:
        print(e)
        return 10