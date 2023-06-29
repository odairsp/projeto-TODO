from flask import Flask, render_template, request
import re
import pymongo
from flask_wtf.csrf import CSRFProtect
import mongoOps
import datetime

app = Flask(__name__)
app.run(debug=True)

app.secret_key = 'd9b766bb3ba3790ad8767d66ce7bf273506b79de73ca8d6b6135fb1f95ee1d43'
csrf = CSRFProtect(app)


@app.route("/", methods={"GET", "POST"})
def login():
    if request.method == "GET":
        return render_template("login.html")

    # VALIDATE LOGIN method POST
    mongoOps.run_migrations()
    erros = []
    form = request.form

    username = form["username"]
    regAlfanum = r'^[a-zA-Z0-9]+$'

    if (not re.search(regAlfanum, username)):
        erros.append("back - Usuario deve ser apenas alfanumerico")

    pwd = form["pwd"]

    regMaiuscula = r'[A-Z]'
    regNumeros = r'[0-9]'
    regEspeciais = r'[!@#$%^&*\(\)_+-=]'

    if (not re.search(regMaiuscula, pwd) and
        not re.search(regEspeciais, pwd) and
            not re.search(regNumeros, pwd)):
        erros.append("back - Senha invalida")

    if len(erros) > 0:

        return render_template("login.html", erros=erros)

    if mongoOps.valida_user(username, pwd):

        erros.append("back - Usuário não encontrado")
        return render_template("login.html", erros=erros)


@app.route("/user/create", methods={"GET", "POST"})
def create():
    if request.method == "GET":
        return render_template("create.html")

    form = request.form

    mongoOps.create_user(form["username"], form["pwd"])
    return render_template("login.html")


@app.route("/index", methods={"GET", "POST"})
def index():

    form = request.form
    if (request.method == "POST" and mongoOps.valida_user(form["username"], form["pwd"])):
        atividades = mongoOps.busca_ativit(form["username"])
        return render_template("index.html", atividades=atividades)

    return render_template("login.html")


@app.route("/create/ativit", methods={"GET", "POST"})
def ativit():
    if (request.method == "GET"):
        
        return render_template("createAtivit.html")

    form = request.form
    mongoOps.create_ativit(form["ativitname"],form["date"],form["username"])
    atividades = mongoOps.busca_ativit(form["username"])

    return render_template("index.html", atividades=atividades)


@app.route("/usuario")
def usuario():
    return "<p>Usuário</p>"
