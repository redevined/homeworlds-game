#!/usr/bin/env python

from flask import *
import user

app = Flask(__name__)
app.secret_key = "9db5ad9c28b20b168144b6e14668b248f26cfc35"


@app.route("/")
def home() :
    return render_template("home.html")

@app.route("/play")
def play() :
    if not session.get("user") :
        return redirect("/login")
    return "You will find the game here. Not yet, someday."

@app.route("/login", methods=["GET", "POST"])
def login() :
    if request.method == "POST" :
        session["user"] = user.getByLogin(request.form)
        if session["user"] :
            return redirect("/play")
        else :
            flash("Incorrect username or password.")
    return render_template("login.html")

@app.route("/logout")
def logout() :
    if session.get("user") :
        session.pop("user")
        flash("You have been logged out succesfully.")
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register() :
    if request.method == "POST" :
        session["user"] = user.getByRegister(request.form)
        if session["user"] :
            return redirect("/play")
        else :
            flash("Failed to create your account. If you haven't left any blank fields, the username might be already taken.")
    return render_template("register.html")

@app.route("/rules")
def rules() :
    return "The first rule of this game is the first rule of this game."

@app.route("/about")
def about() :
    return "This is a page about this page."


if __name__ == "__main__" :
    app.run(debug = True)
