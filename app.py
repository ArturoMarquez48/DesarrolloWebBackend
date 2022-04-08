#from crypt import methods
from flask import Flask, render_template, request

# FlASK
#############################################################
app = Flask(__name__)
#############################################################

@app.route('/')
def home():
    return render_template('index.html')

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
    if(request.method == "GET"):
        email = None
        return render_template('Login.html', error = email)
    else:
        email = request.form["email"]
        password = request.form["password"]
        return render_template('index.html', error = email)

#Página para el signup.
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if(request.method == "GET"):
        email = None
        return render_template('Login.html', error = email)
    else:
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        return render_template('index.html', error = email)
