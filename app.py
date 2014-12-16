#!/usr/bin/env python

import os
from flask import *
import user

# Create app
app = Flask(__name__)
# Secret key for sessions
app.secret_key = os.urandom(32)
# Provide User.isAdmin method in views
app.jinja_env.globals.update(
    userIsAdmin = lambda sid : user.getBySession(sid).isAdmin() if user.getBySession(sid) else False
)



# Homepage
@app.route("/")
def home() :
    return render_template("home.html")

# Entry pages for games if loggeed in, else redirects to login
@app.route("/play")
def play() :
    if not session.get("user") :
        return redirect("/login")
    return render_template("portal.html")

# Action for login page
@app.route("/login", methods=["GET", "POST"])
def login() :
    if request.method == "POST" :
        session["user"] = user.getByLogin(request.form)
        if session["user"] :
            return redirect("/play")
        else :
            flash("Incorrect username or password.")
    return render_template("login.html")

# Registers new users or directs them to the register page
@app.route("/register", methods=["GET", "POST"])
def register() :
    if request.method == "POST" :
        session["user"] = user.getByRegister(request.form)
        if session["user"] :
            return redirect("/play")
        else :
            flash("Failed to create your account. If you haven't left any blank fields, the username might be already taken.")
    return render_template("register.html")

# Removes session
@app.route("/logout")
def logout() :
    if session.get("user") :
        user.removeSession(session.pop("user"))
        flash("You have been logged out succesfully.")
    return redirect("/login")

# Admin interface
@app.route("/admin")
def admin() :
    if session.get("user") :
        if user.getBySession(session["user"]).isAdmin() :
            return render_template(
                "admin.html",
                sessions = user.getCurrentUsers(),
                users = user.getAllUsers(),
                games = []
            )
    return redirect("/login")

# Admin functions
@app.route("/admin/<function>/<param>")
def adminFunctions(function, param) :
    if session.get("user") :
        user = user.getBySession(session.get("user"))
        if user.getBySession(session["user"]).isAdmin() :
            if function == "terminate":
                user.removeSession(int(param))
            elif function == "elevate" :
                user.getByName(param).isAdmin(True)
            elif function == "lower" :
                user.getByName(param).isAdmin(False)
            elif function == "delete" :
                user.deleteByName(param)
            return redirect("/admin")
    return redirect("/login")

# Rules page
@app.route("/rules")
def rules() :
    return render_template("rules.html")

# About page
@app.route("/about")
def about() :
    return render_template("about.html")



# Error pages for various http errors
@app.errorhandler(404)
@app.errorhandler(403)
@app.errorhandler(500)
def exception(error) :
    code = error.code
    return render_template("error.html", code = code), code



# Run app if main
if __name__ == "__main__" :
    app.run(debug = True)
