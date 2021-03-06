#!/usr/bin/env python


class Game() :

    def __init__(self, players) :
        self.name = "{}_vs_{}".format(*players)
        self.players = players
        self.active = players[0]
        self.winner = None
        self.homes = dict()
        self.otherPlayer = lambda p : players[players.index(p)-1]
        self.universe = Universe(self)
        self.aproc = ActionProcessor(self)

    def register(self, player, star1, star2, ship) :
        homeid = self.universe.newSystem(star1, star2)
        self.universe.getSystem(homeid).new(player, ship[1], ship[0])
        self.homes[player] = homeid

    def parse(self, cmd) :
        # Parsing strings
        # Attack: "player system red target"
        # Build: "player system green target"
        # Trade: "player system blue target color"
        # Move: "player system yellow target system"
        # Discover (Move): "player system yellow target color size"
        # Sacrifice: "player system sacrifice target" + target.size*action(target.color)
        # Cataclysm: "player system cataclysm"
        # Pass: "player pass"

        proc = cmd.split()
        player, sys, action = proc[0:3]

        if action == "s" :
            self.aproc.sacrifice(player, sys, proc[3])
            procs = [[player] + f.split() for f in " ".join(proc[4:]).split(player)][1:]
            for proc in procs :
                self.parse(" ".join(proc))
        elif action == "y" and len(proc) > 5 :
            self.aproc.discover(player, sys, *proc[3:])
        elif action == "p" :
            pass
        else :
            {
                "r" : self.aproc.attack,
                "g" : self.aproc.build,
                "b" : self.aproc.trade,
                "y" : self.aproc.move,
                "c" : self.aproc.cataclysm
            }[action](player, int(sys), *proc[3:])

        self.winner = self.finish(player)

    def finish(self, player) :
        win = list()
        for p, homeid in self.homes.items() :
            try :
                if not self.universe.getSystem(homeid).areas[p] :
                    win.append(self.otherPlayer(p))
            except KeyError :
                win.append(self.otherPlayer(p))
        self.active = self.otherPlayer(player)
        return win or None


class ActionProcessor() :

    def __init__(self, inst) :
        self.game = inst

    def attack(self, player, sys, target) :
        system = self.game.universe.getSystem(sys)
        ship = system.get(self.game.otherPlayer(player), target[1], target[0])
        system.add(player, ship)

    def build(self, player, sys, target) :
        system = self.game.universe.getSystem(sys)
        system.new(player, target[1], target[0])

    def trade(self, player, sys, target, color) :
        system = self.game.universe.getSystem(sys)
        system.remove(player, target[1], target[0])
        system.new(player, target[1], color)

    def move(self, player, sys, target, nsys) :
        system = self.game.universe.getSystem(sys)
        ship = system.get(player, target[1], target[0])
        system = self.game.universe.getSystem(nsys)
        system.add(player, ship)

    def discover(self, player, sys, target, color, size) :
        system = self.game.universe.getSystem(sys)
        ship = system.get(player, target[1], target[0])
        system = self.game.universe.newSystem((color, size))
        system.add(player, ship)

    def sacrifice(self, player, sys, target) :
        system = self.game.universe.getSystem(sys)
        system.remove(player, target[1], target[0])

    def cataclysm(self, player, sys) :
        system = self.game.universe.getSystem(sys)
        def catagen(*elements) :
            elements = [e.color for es in elements for e in es]
            for c in ("r", "g", "b", "y") :
                if elements.count(c) >= 4 :
                    yield c

        for c in catagen(system.areas.values()) :
            for a, p in system :
                for e in a :
                    if e.color == c :
                        system.remove(p, e.color, e.size)

        if not system["star"] :
            self.game.universe.removeSystem(sys)


class Universe() :

    def __init__(self, inst) :
        self.game = inst
        self.systems = dict()
        self.stash = Stash()

    def __iter__(self) :
        for sysid, system in self.systems.items() :
            yield system, sysid

    def newSystem(self, *stars) :
        sys = System(self, stars)
        sysid = max(self.systems.keys()) + 1 if len(self.systems) > 0 else 100
        self.systems[sysid] = sys
        return sysid

    def getSystem(self, sysid) :
        return self.systems[sysid]

    def removeSystem(self, sysid) :
        del(self.systems[sysid])


class System() :

    def __init__(self, inst, stars) :
        self.universe = inst
        self.areas = {"star": [], inst.game.players[0]: [], inst.game.players[1]: []}
        for star in stars :
            self.new("star", star[1], star[0])

    def __getitem__(self, key) :
        return self.areas[key]

    def __iter__(self) :
        for p, area in self.areas.items() :
            yield area, p

    def __del__(self) :
        for p, a in self.areas :
            for e in a :
                self.remove(p, e.color, e.size)

    def new(self, player, color, size) :
        element = self.universe.stash.get(color, size)
        self.add(player, element)

    def add(self, player, element) :
        self.areas[player].append(element)

    def get(self, player, color, size) :
        element = self.areas[player].pop([str(e) for e in self.areas[player]].index(size + color))
        return element

    def remove(self, player, color, size) :
        element = self.get(player, color, size)
        self.universe.stash.add(element)


class Stash() :

    def __init__(self, size = 5) :
        self.stacks = { c : {
            s : [Element(c, s) for i in range(size)] for s in ("1", "2", "3")
        } for c in ("r", "g", "b", "y") }

    def add(self, element) :
        self.stacks[element.color][element.size].append(element)

    def get(self, color, size) :
        return self.stacks[color][size].pop()


class Element() :

    def __init__(self, color, size) :
        self.color = color
        self.size = size

    def __str__(self) :
        return str(self.size) + self.color
