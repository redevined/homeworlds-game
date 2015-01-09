#!/usr/bin/env python

class Game() :

    def __init__(self, player1, player2) :
        self.players = [player1, player2]
        self.universe = Universe()

    def parse(self, pstr) :
        pass


class Universe() :

    def __init__(self) :
        self.systems = list()
        self.stash = Stash()

    def addSystem(self, *stars, home = None) :
        self.systems.append(System(stars, home))


class System() :

    def __init__(self, stars, home) :
        self.star = stars
        self.area1 = []
        self.area2 = []
        self.home = home

    def __del__(self) :
        if self.home is not None :
            pass


class Stash() :

    def __init__(self, size = 5) :
        self.stacks = { c : { s : [Element(c, s) for i in range(size)] for s in (1, 2, 3) } for c in ("r", "g", "b", "y") }


class Element() :

    def __init__(self, color, size) :
        self.type = None
        self.color = color
        self.size = size

    def isShip(self, enable = False) :
        if enable :
            self.type = "ship"
        return self.type == "ship"

    def isStar(self, enable = False) :
        if enable :
            self.type = "star"
        return self.type == "star"
