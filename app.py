#!/usr/bin/env python

from flask import *
app = Flask(__name__)

@app.route("/")
def home() :
    return render_template("home.html")

@app.route("/play")
def play() :
    if not session.get("logged_in") :
        return redirect("/login")
    return "You will find the game here. Not yet, someday."

@app.route("/login", methods=["GET", "POST"])
def login() :
    if request.method == "POST" :
        if request.form["username"] == "admin" and request.form["password"] == "1234" :
            return "Nice try."
    return render_template("login.html")

@app.route("/rules")
def rules() :
    return "The first rule of this game is the first rule of this game."

@app.route("/about")
def about() :
    return "This is a page about this page."

if __name__ == "__main__" :
    app.run(debug = True)
