#from crypt import methods
from datetime import datetime
import email
from email import message
from re import T
from unicodedata import name
from flask import Flask, redirect, render_template, request, session, url_for
import datetime
from pkg_resources import require
import pymongo
from twilio.rest import Client
from decouple import config
from sqlalchemy import true



# FlASK
#############################################################
app = Flask(__name__)
#Con las siguientes lineas se puede mantener la sesión del usuario por un año.
app.permanent_session_lifetime = datetime.timedelta(days=365)
#Con esta llave, la sesión queda encriptada.
app.secret_key = "super secret key"
#############################################################

# MONGODB
#############################################################
client = pymongo.MongoClient(
    config("mongodb_key"), tls=True, tlsAllowInvalidCertificates=True)
db = client.app
cuentas = db.usuarios
#############################################################


# Twilio
#############################################################
account_sid = config("account_sid")
auth_token = config("auth_token")
TwilioClient = Client(account_sid, auth_token)
#############################################################


@app.route('/')
def home():
    #Si sí está el email en la sesión, lo manda al index.
    email = None
    if cuentas in session:
        email = session["email"]
        return render_template('index.html', data = email)
    else:
        return render_template("Login.html", data = None)


@app.route('/prueba')
def prueba():
    return ("A01376086")


# Prueba dos donde probamos el acceso a otra librería Jinja.
@app.route('/prueba2')
def prueba2():
    nombres = []
    nombres.append({"nombre": "Ruben", 
    "Semestre01": [{
        "matematicas": "10", "español": "10"
    }],
    "Semestre02": [{
        "programacion": "9", "basededatos": "7"
    }]})
    nombres.append({"nombre": "Sergio"})
    return render_template("home.html", data=nombres)


#Página para el login.
@app.route("/login", methods=["GET", "POST"])
def login():
    email = None
    if cuentas in session:
        return render_template('index.html', data = session["email"])
        #return redirect(url_for("home"))
    else:
        email = request.form["email"]
        password = request.form["password"]
        busqueda = cuentas.find_one({"email": (email), "password": (password)})
        if busqueda == None:
            return render_template('Login.html', data = None)
        else:
            session["email"] = email
            return render_template('index.html', data = session["email"])



#Página para el signup.
@app.route("/signup", methods=["GET", "POST"])
def signup():
    email = None
    if(request.method == "GET"):
        return render_template('Login.html', data = session["email"])
    else:
        user = {
            "name": request.form["name"],
            "email": request.form["email"],
            "password": request.form["password"],
        }
        email = request.form["email"]
        busqueda = cuentas.find_one({"email": (email)})
        if busqueda == None:
            try:
                cuentas.insert_one(user)
                message = TwilioClient.messages.create(
                    from_='whatsapp:+14155238886',
                    body="El usuario %s se agregó a tu pagina web" % (
                        request.form["name"]), 
                        to='whatsapp:+5215529037543'
                )
                session["email"] = email
                print(message.sid)
                return render_template('index.html', data = session["email"])
            except Exception as e:
                return "<p> El servicio no está disponible =>: %s." % (e)
        else:
            return render_template('Login.html', data = None)


#Ruta para el logout.
@app.route("/logout")
def logout():
    if 'email' in session:
        email = session['email']
    session.clear()
    return redirect(url_for('home'))

@app.route("/usuarios")
def usuarios():
    cursor = cuentas.find({})
    users = []
    for doc in cursor:
        users.append(doc)
    return render_template("/usuarios.html", data=users)


@app.route("/insert", methods = ["POST"])
def insertUsers():
    user = {
        "matricula": request.form["matricula"],
        "nombre": request.form["nombre"],
        "correo": request.form["correo"],
        "contrasena": request.form["contrasena"]
    }

    try:
        cuentas.insert_one(user)
        # message = TwilioClient.messages.create(
        #     from_="whatsapp:+14155238886",
        #     body="El usuario %s se agregó a tu pagina web" % (
        #         request.form["nombre"]),
        #     to="whatsapp:+5215514200581"
        # )
        return redirect(url_for("usuarios"))
    except Exception as e:
        return "<p> El servicio no está disponible =>: %s %s." % type(e), e
    

@app.route("/find_one/<matricula>")
def find_one(matricula):
    try:
        user = cuentas.find_one({ "matricula": (matricula) })
        if user == None:
            return "<p> La matricula %s no existe en Monguito</p>" % (matricula)
        else:
            return "<p> Encontramos: %s </p>" % (user)
    except Exception as e:
        return " %s " % e


@app.route("/delete_one/<matricula>")
def delete_one(matricula):
    try:
        user = cuentas.delete_one({ "matricula": (matricula) })
        if user.deleted_count == 0: # O sea que no borró nada
            return "<p> La matricula %s no existe en Monguito</p>" % (matricula)
        else:
            return redirect(url_for("usuarios"))
    except Exception as e:
        return " %s " % e


@app.route("/update", methods=["POST"])
def update():
    try:
        filter = {"matricula": request.form["matricula"]} #Primero crea un filtro de busqueda.
        user = {"$set": {
            "nombre": request.form["nombre"],
            "constrasena": request.form["contrasena"]
        }}
        cuentas.update_one(filter, user)
        return redirect(url_for("usuarios"))

    except Exception as e:
        return " %s " % e


@app.route("/create")
def create():
    return render_template("createForm.html")