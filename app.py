#!/usr/bin/env python

import os
from flask import *
import user

app = Flask(__name__)
app.secret_key = os.urandom(32)
app.jinja_env.globals.update(getUser = user.getBySession)


@app.route("/")
def home() :
    return render_template("home.html")

@app.route("/play")
def play() :
    if not session.get("user") :
        return redirect("/login")
    return render_template("portal.html")

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
        del session["user"]
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

@app.route("/admin")
def admin() :
    if session.get("user") :
        if user.getBySession(session["user"]).isAdmin() :
            return render_template(
                "admin.html",
                users=user.getAllUsers(),
                games=[]
            )
    return redirect("/login")

@app.route("/rules")
def rules() :
    return render_template("rules.html")

@app.route("/about")
def about() :
    return render_template("about.html")

@app.route("/hobbits")
def debug() :
    for ses in session :
        print session
    return "<h2>They're taking the hobbits to Isengard!</h2>"


@app.errorhandler(404)
@app.errorhandler(403)
@app.errorhandler(500)
def exception(error) :
    code = error.code
    return render_template("error.html", code = code), code


if __name__ == "__main__" :
    app.run(debug = True)
