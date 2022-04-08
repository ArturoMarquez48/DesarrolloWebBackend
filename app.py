#from crypt import methods
from datetime import datetime
import email
from flask import Flask, redirect, render_template, request, session, url_for
import datetime

# FlASK
#############################################################
app = Flask(__name__)
#Con las siguientes lineas se puede mantener la sesión del usuario por un año.
app.permanent_session_lifetime = datetime.timedelta(days=365)
#Con esta llave, la sesión queda encriptada.
app.secret_key = "super secret key"
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
    