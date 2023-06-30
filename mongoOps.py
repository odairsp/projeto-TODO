# definição do schema

import pymongo
from flask import session
from pymongo.server_api import ServerApi

# Lib para fazer url-encode
import urllib.parse
# bcript
import bcrypt

import datetime

userSchema = {
    '$jsonSchema': {
        'bsonType':'object',
        'title':'User Object Validation',
        'required': ['username','password'],
        'properties': {
            'username': {'bsonType':'string'},
            'password': {'bsonType':'binData'}
        }
    }
}
ativitSchema = {
    '$jsonSchema': {
        'bsonType':'object',
        'title':'User Object Validation',
        'required': ['ativitname','date', 'username'],
        'properties': {
            'ativitname': {'bsonType':'string'},
            'date': {'bsonType':'Date'},
            'username': {'bsonType':'string'}
        }
    }
}

# 1- criar a url de acesso mongodb
# 2- iniciar o client compymongo
# 3- carregar o banco 

url_cluster = "mongodb+srv://dba:Dba123456@odr.ookqkat.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(url_cluster,server_api=ServerApi('1'))
db = client["ssidbiii"]

def run_migrations():
    db.list_collection_names()
    if not "usuarios" in db.list_collection_names():
        db.create_collection("usuarios", validator=userSchema)
    if not "atividades" in db.list_collection_names():
        db.create_collection("atividades", validator=ativitSchema)

def create_user(usuario, senha):
    run_migrations()
    if db["usuarios"].find_one({"username" : usuario}):
        return False
    usuario = urllib.parse.quote(usuario)
    senha = urllib.parse.quote(senha)

    senha_bytes = senha.encode("utf-8")
    salt = bcrypt.gensalt()
    senha_hash = bcrypt.hashpw(senha_bytes, salt)
    
    return db["usuarios"].insert_one({"username": usuario, "password" : senha_hash })


def create_ativit(ativitname, date, username):
    
    if db["atividades"].find_one({"ativitname" : ativitname}):
        return False
    
    ativitname = urllib.parse.quote(ativitname)
    username = urllib.parse.quote(username)
   
    return db["atividades"].insert_one({"ativitname": ativitname, "date" : date, "username": username})


def busca_user(usuario):
    usuario = urllib.parse.quote(usuario)
    
    resposta = db["usuarios"].find_one({"username":usuario})
    
    if not resposta:
        return False
    return resposta

def busca_ativit(usuario):
    usuario = urllib.parse.quote(usuario)
    
    resposta = db["atividades"].find({"username":usuario})
    
    if not resposta:
        return False
    

    return resposta

def valida_user(usuario, senha):
    usuario = busca_user(usuario)

    if not usuario:
        return False
 
    senha = urllib.parse.quote(senha)
    if bcrypt.checkpw(senha.encode('utf-8'), usuario["password"]):
        session["username"] = usuario["username"]
        return True
    return False