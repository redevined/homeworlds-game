#!/usr/bin/env python

class Game() :

    def __init__(self, player1, player2) :
        self.players = [player1, player2]
        self.active = 0
        self.universe = Universe()
        self.aproc = ActionProcessor(self)

    def parse(self, pstr) :
        # Parsing strings
        # Attack: "player system red target"
        # Build: "player system green color"
        # Trade: "player system blue target color"
        # Move: "player system yellow target system"
        # Discover (Move): "player system yellow target color size"
        # Sacrifice: "player system sacrifice target" + target.size*action(target.color)
        # Cataclysm: "player system cataclysm"
        # Pass: "player pass"

        proc = pstr.split()
        player = self.players.index(proc[0])
        sys = proc[1]
        action = proc[2]

        if action == "s" :
            n = aproc.sacrifice(player, sys, proc[3])
            procs = [[player] + f.split() for f in " ".join(proc[4:]).split(player)][1:]
            for proc in procs :
                self.parse(" ".join(proc))

        elif action == "y" and len(proc) > 5 :
            aproc.discover(player, sys, *proc[3:])
        elif action == "p" :
            pass
        else :
            {
                "r" : aproc.attack,
                "g" : aproc.build,
                "b" : aproc.trade,
                "y" : aproc.move,
                "c" : aproc.cataclysm
            }[action](player, sys, *proc[3:])

        self.active = (player + 1) % 2


class ActionProcessor() :

    def __init__(self, inst) :
        self.game = inst

    def attack(self, player, sys, target) :
        pass

    def build(self, player, sys, color) :
        pass

    def trade(self, player, sys, target, color) :
        pass

    def move(self, player, sys, target, nsys) :
        pass

    def discover(self, player, sys, target, color, size) :
        pass

    def sacrifice(self, player, sys, target) :
        pass

    def cataclysm(self, player, sys) :
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
