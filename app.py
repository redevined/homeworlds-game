#!/usr/bin/env python

import os
from flask import *
import user

app = Flask(__name__)
app.secret_key = os.urandom(32)


@app.route("/")
def home() :
    return render_template("home.html")

@app.route("/play")
def play() :
    if not session.has_key("user") :
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
    if session.has_key("user") :
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
    if session.has_key("user") :
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

@app.route("/debug")
def debug() :
    return "Successfully executed command."


if __name__ == "__main__" :
    app.run(debug = True)
