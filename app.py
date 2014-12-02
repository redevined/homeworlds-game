#!/usr/bin/env python

from flask import Flask
app = Flask(__name__)

@app.route("/")
def home() :
    return "It works, bitches."

@app.route("/play")
def join() :
    return "You will find the game here. Not yet, someday."

@app.route("/play/<int:gameID>")
def play(gameID) :
    return "Looking for game #" + gameID + "? Obviously not here."

@app.route("/rules")
def rules() :
    return "The first rule of this game is the first rule of this game."

@app.route("/about")
def about() :
    return "This is a page about this page."

if __name__ == "__main__" :
    app.run(debug = True)
