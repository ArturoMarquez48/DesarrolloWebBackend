#from crypt import methods
from datetime import datetime
import email
from re import T
from flask import Flask, redirect, render_template, request, session, url_for
import datetime
import pymongo

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
mongodb_key = "mongodb+srv://desarrollowebuser:desarrollowebpassword@cluster0.dfh7g.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(
    mongodb_key, tls=True, tlsAllowInvalidCertificates=True)
db = client.Escuela
cuentas = db.alumno
#############################################################



@app.route('/')
def home():
    #Si sí está el email en la sesión, lo manda al index.
    email = None
    if "email" in session:
        email = session["email"]
        return render_template('index.html', data = "email")
    else:
        return render_template("Login.html", data = email)

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
    if "email" in session:
        return render_template('index.html', data = session["email"])
        #return redirect(url_for("home"))
    else: 
        if(request.method == "GET"):
            return render_template('Login.html', data = email)
        else:
            email = request.form["email"]
            password = request.form["password"]
            #Asignamos un correro adentro de la sesión.
            session["email"] = email
            return render_template('index.html', data = email)


#Página para el signup.
@app.route("/signup", methods=["GET", "POST"])
def signup():
    email = None
    if(request.method == "GET"):
        return render_template('Login.html', data = email)
    else:
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        return render_template('index.html', data = email)


#Ruta para el logout.
@app.route("/logout")
def logout():
    if "email" in session:
        session.clear()
        return redirect(url_for("home"))


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