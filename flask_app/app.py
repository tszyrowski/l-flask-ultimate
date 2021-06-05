from flask import Flask, jsonify, request, url_for, redirect, session

app = Flask(__name__)

app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "thisisasecret"

@app.route("/")
def base():
    return "<h1>Hello from home page</h1>"

@app.route("/home", methods=["POST", "GET"], defaults={"name": "Default"})
@app.route("/home/<string:name>", methods=["POST", "GET"])
def home(name):
    session["name"] = name
    return f"<h1>Hello {name} It is a Home page</h1>"

@app.route("/json", methods=["POST", "GET"])
def json():
    if "name" in session:
        name = session["name"]      # /home must be refreshed in the browser
    else: name = "NOT In Session"   # also removing anywhere in the code
    return jsonify({"key": "value", "listkey": [1,2,3], "name": name})

@app.route('/<name>')
def index(name):
    mylist = [1,2,3,4]
    foo = session["foo"]
    return f'<h1>Hello {name}! :) {foo}</h1>'

@app.route("/query")
def query():
    name = request.args.get("name")
    location = request.args.get("location")
    return f"<h1>Hi {name}, You are from {location} You are on the query page</h1>"

@app.route("/theform")
def theform():
    return """<form method="POST" action="/process">
                <input type="text" name="name">
                <input type="test" name="location">
                <input type="submit" value="Submit">
            </form>"""

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
    return jsonify({"result": "success", "name": name, "location": location, "list": randomlist})

@app.route("/combinedform", methods=["GET", "POST"])
def combinedform():
    if request.method == "POST":
        name = request.form["name"]
        location = request.form["location"]
        return f"<h1>OTHER FORM {name}. YOu are from {location}. Form submitted</h1>"
    return """<form method="POST">
                  <div><label>Name: <input type="text" name="name"></label></div>
                  <div><label>Location: <input type="text" name="location"></label></div>
                  <input type="submit" value="Submit">
              </form>"""

@app.route("/redirect", methods=["GET", "POST"])
def redirection():
    if request.method == "POST":
        name = request.form["name"]
        location = request.form["location"] # will be in query string http://127.0.0.1:5000/home/nn?location=k
        return redirect(url_for("home", name=name, location=location))

    return """<form method="POST">
                  <div><label>REdirect: <input type="text" name="name"></label></div>
                  <div><label>Anyway: <input type="text" name="location"></label></div>
                  <input type="submit" value="Submit">
              </form>"""

