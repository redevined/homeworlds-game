#!/usr/bin/env python

import os
import cPickle as serializer
import homeworlds


def saveGame(game) :
    path = os.path.join("games", game.name + ".p")
    with open(path, "w") as f :
        serializer.dump(game, f)

def openGame(name) :
    path = os.path.join("games", name + ".p")
    if os.path.exists(path) :
        with open(path, "r") as f :
            return serializer.load(f)
    return None

def newGame(users) :
    game = homeworlds.Game([user.username for user in users])
    for user in users :
        user.games.append(game.name)
    saveGame(game)
    return game.name

def finishGame(name) :
    os.remove(os.path.join("games", name + ".p"))

def render(game, template) :
    gameUI = "gameUI.html"
    return template(gameUI, game = game)

def getAllGames() :
    return [openGame(path.rsplit(".", 1)[0]) for path in os.listdir("games")]
