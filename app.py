from flask import Flask
from flask_bootstrap import Bootstrap
from flask import request, render_template , redirect, jsonify
import json
import pandas as pd

app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def home():
    return redirect("/showGestures/")

@app.route("/on/")
def on():
    return "Everything is on."

@app.route("/off/")
def off():
    return "Everything is off"

@app.route("/get_json/")
def get_json():
    with open("map.json", "r") as f:
        data = json.load(f)
    return jsonify(data)


@app.route("/showGestures/")
def gesture_tab():
    with open("map.json") as f:
        table= json.loads(f.read())
    return render_template("mapper.html", table=table )

@app.route("/modify/<gesture>", methods=['GET', 'POST'])
def modify_gesture(gesture):
    if request.method == "POST":
        with open ("map.json", "r") as f:
            data = json.load(f)
            data[gesture] = request.form['action']
        with open("map.json", 'w') as f:
            f.write(json.dumps(data)) 
        return redirect("/showGestures/")
    else:
        # return """
        # {% extends "bootstrap/base.html" %}
        # <div style=" background: linear-gradient(to bottom, #123e5c, #7bdef8);  text-align: center; height: 100%">
        # <div class="container">
        # <h3 > Change action for {gesture} <br> </h3>
        # <form  method="post">
        #  <div class="form-group">
        #  <p> <input class="form-control" type=text name=action>
        #  <p> <input class="form-control" type=submit value=Change></div>
        #  </form></div></div>
        #  """.format(gesture=gesture)
        return render_template("form.html", gesture=gesture )
