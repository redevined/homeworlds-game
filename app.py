#!/usr/bin/env python

import os, random
from flask import *

# User management and authentication decorators + game control functions
import userInterface as user
import gameInterface as game

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


# Entry page for games
@app.route("/play", methods=["GET", "POST"])
@user.auth
def play() :
    if request.method == "POST" :
        players = (
            user.getBySession(session.get("user")),
            user.getByName(request.form["username"]) if request.form["username"].lowercase() != "random"
                else random.choice(user.getAllUsers())
        )
        if None not in players :
            return redirect("/play/" + game.newGame(players))
        else :
            flash("There is no user with this name.")
    return render_template("portal.html", games = user.getBySession(session.get("user")).games)

# Continue existing game
@app.route("/play/<param>", methods=["GET", "POST"])
@user.auth
def playGame(param) :
    gg = game.openGame(param)
    if request.method == "POST" :
        gg.parse(request.form["command"])
        game.saveGame(gg)
    return render_template("gameUI.html", **game.render(gg, user.getBySession(session.get("user"))))


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
@user.auth
def logout() :
    user.removeSession(session.pop("user"))
    flash("You have been logged out succesfully.")
    return redirect("/login")


# Admin interface
@app.route("/admin")
@user.authAdmin
def admin() :
    return render_template(
        "admin.html",
        sessions = user.getCurrentUsers(),
        users = user.getAllUsers(),
        games = game.getAllGames()
    )

# Admin functions
@app.route("/admin/<function>/<param>")
@user.authAdmin
def adminFunctions(function, param) :
    if function == "terminate":
        user.removeSession(int(param))
    elif function == "elevate" :
        user.getByName(param).isAdmin(True)
    elif function == "lower" :
        user.getByName(param).isAdmin(False)
    elif function == "delete" :
        user.deleteByName(param)
    elif function == "stop" :
        game.finishGame(name)
    return redirect("/admin")


# Rules page
@app.route("/rules")
def rules() :
    return render_template("rules.html")

# About page
@app.route("/about")
def about() :
    return render_template("about.html")
    #return render_template("about.html")


# Error pages for various http errors
@app.errorhandler(404)
@app.errorhandler(403)
@app.errorhandler(500)
def exception(error) :
    code = error.code
    return render_template("error.html", code = code), code


# DO NOT USE IN PRODUCTIVE ENVIRONMENT
@app.route("/debug")
def debug() :
    cmd = "print 'Homeworlds-online app hacking CLI, use with caution!'"
    while cmd :
        exec cmd
        cmd = raw_input(">>> ")
    return "{ accomplished : true }"


# Run app if main
if __name__ == "__main__" :
    app.run(debug = True)
