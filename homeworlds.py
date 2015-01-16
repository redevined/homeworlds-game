#!/usr/bin/env python

class Game() :

    def __init__(self, *players) :
        self.players = players
        self.active = players[0]
        self.otherPlayer = lambda p : players[players.index(p)-1]
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
        player = proc[0]
        sys = proc[1]
        action = proc[2]

        if action == "s" :
            aproc.sacrifice(player, sys, proc[3])
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

        self.active = self.otherPlayer(player)


class ActionProcessor() :

    def __init__(self, inst) :
        self.game = inst

    def attack(self, player, sys, target) :
        system = self.game.universe.getSystem(sys)
        ship = system.take(self.game.otherPlayer(player), target)
        system.add(player, ship)

    def build(self, player, sys, color) :
        system = self.game.universe.getSystem(sys)
        system.addShip(player, color)

    def trade(self, player, sys, target, color) :
        system = self.game.universe.getSystem(sys)
        ship = system.take(player, target)
        stash.add(ship)
        ship = self.game.stash.take("ship", color, ship.size)
        system.add(player, ship)

    def move(self, player, sys, target, nsys) :
        system = self.game.universe.getSystem(sys)
        ship = system.take(player, target)
        system = self.game.universe.getSystem(nsys)
        system.add(player, ship)

    def discover(self, player, sys, target, color, size) :
        system = self.game.universe.getSystem(sys)
        ship = system.take(player, target)
        system = self.game.universe.newSystem(color, size)
        system.add(player, ship)

    def sacrifice(self, player, sys, target) :
        system = self.game.universe.getSystem(sys)
        ship = system.take(player, target)
        stash.add(ship)

    def cataclysm(self, player, sys) :
        system = self.game.universe.getSystem(sys)



class Universe() :

    def __init__(self, inst) :
        self.game = inst
        self.systems = list()
        self.stash = Stash()

    def addSystem(self, *stars, home = None) :
        self.systems.append(System(stars, home))


class System() :

    def __init__(self, inst, stars, home) :
        self.universe = inst
        self.areas = {"star": stars, inst.game.players[0]: [], inst.game.players[1]: []}
        self.home = home

    def __del__(self) :
        if self.home is not None :
            pass

    def newShip(self, player, color, size = None) :
        ship = self.universe.stash.take(color, size)
        self.areas[player].append(ship)

    def addShip(self, player, ship) :
        self.areas[player].append(ship)

    def takeShip(self, player, shipstr) :
        ship = self.areas[player].pop([str(s) for f in self.areas[player]].index(shipstr))
        return ship


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
