from flask import (
    Flask, jsonify, request, url_for, redirect, session, render_template, g
)
import sqlite3

app = Flask(__name__, template_folder="../templates")

app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "thisisasecret"

def connect_db():
    """Connect to database funciton"""
    sql = sqlite3.connect(
        "/home/t/trainingWorkspace/flask_ultimate_orelly/database/data.db"
    )
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    """Get database when needed and store in global var."""
    if not hasattr(g, "sqlite3"):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Close db connection to prevent memorey leaks.
    
    Called whenever route returns.
    """
    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close()

@app.route("/")
def base():
    return "<h1>Hello from home page</h1>"

@app.route("/home", methods=["POST", "GET"], defaults={"name": "Default"})
@app.route("/home/<string:name>", methods=["POST", "GET"])
def home(name):
    session["name"] = name
    display = False
    if name[0].lower() in ["t", "a", "e", "i", "o", "u", "y"]:
        display = True
    
    db = get_db()
    cur = db.execute("select id, name, location from users")
    results = cur.fetchall()

    return render_template(
        "home.html",
        name=name,
        display=display,
        letters = [l for l in name],
        results = results,
        listDicts = {k:(name.index(k)+1)*2 for k in name}
    )

@app.route("/json", methods=["POST", "GET"])
def json():
    if "name" in session:
        name = session["name"]      # /home must be refreshed in the browser
    else: name = "NOT In Session"   # also removing anywhere in the code
    return jsonify({"key": "value", "listkey": [1,2,3], "name": name})

@app.route('/<name>')
def index(name):
    mylist = [1,2,3,4]
    foo = None
    if "foo" in session:
        foo = session["foo"]
    return f'<h1>Hello {name}! :) {foo}</h1>'

@app.route("/query")
def query():
    name = request.args.get("name")
    location = request.args.get("location")
    return f"<h1>Hi {name}, You are from {location} " \
        "You are on the query page</h1>"

@app.route("/theform")
def theform():
    return render_template("basic_form.html")

@app.route("/process", methods=["POST"])
def process():
    name = request.form["name"]
    location = request.form["location"]
    return f"<h1>Hello {name}. YOu are from {location}. Form submitted</h1>"

@app.route("/processjson", methods=["POST"])
def processjson():
    data = request.get_json()
    name = data["name"]
    location = data["location"]
    randomlist = data["randomlist"]
    return jsonify(
        {
            "result": "success",
            "name": name,
            "location": location,
            "list": randomlist
        }
    )

@app.route("/combinedform", methods=["GET", "POST"])
def combinedform():
    if request.method == "POST":
        name = request.form["name"]
        location = request.form["location"]
        return f"<h1>OTHER FORM {name}. You're from {location}. Submitted</h1>"
    return render_template("fmt_form.html")

@app.route("/redirect", methods=["GET", "POST"])
def redirection():
    if request.method == "POST":
        name = request.form["name"]
        # will be in query string http://127.0.0.1:5000/home/nn?location=k
        location = request.form["location"] 
        return redirect(url_for("home", name=name, location=location))

    return render_template("fmt_form.html")

@app.route("/viewresults")
def viewresutls():
    db = get_db()
    cur = db.execute("select id, name, location from users")
    results = cur.fetchall()
    returned_string = ""
    for result in results:
        entry = f"<h1>The ID is {result['id']}, the name is {result['name']}," \
            f" location is {result['location']}</h1>"
        returned_string += entry
    return returned_string

@app.route("/addresults", methods=["GET", "POST"])
def addresults():
    if request.method == "POST":
        name = request.form["name"]
        location = request.form["location"]

        db = get_db()
        db.execute(
            "insert into users (name, location) values (?, ?)",
            [name, location]
        )
        db.commit()

        return f"<h1>Added to DB: {name}. from {location}. Submitted</h1>"
    return render_template("fmt_form.html")