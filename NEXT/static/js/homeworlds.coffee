#!/usr/bin/env coffee


# Player object
class Player

	constructor: (current) ->
		@id = current.id
		@name = current.name
		@actions = current.actions

	isActive: () ->
		@actions != 0


# Base class of all drawable objects
class Element

	constructor: (e) ->
		@e = $(e)

	render: (surface) ->
		surface.append(@e)

	remove: () ->
		@e.detach()


# Container for unused game pieces
class Stash extends Element

	constructor: (current) ->
		@stack = {
			red: ((new Stashed(s) for s in current.red[i]) for i in [0..2]),
			green: ((new Stashed(s) for s in current.green[i]) for i in [0..2]),
			blue: ((new Stashed(s) for s in current.blue[i]) for i in [0..2]),
			yellow: ((new Stashed(s) for s in current.yellow[i]) for i in [0..2])
		}
		super("""
			<div id="stash-wrapper">
				<table id="stash">
				</table>
			</div>
		""")

	render: (surface) ->
		for color, shipgroups of @stack
			tr = $("""<tr class="stash-#{color}"></tr>""")
			size = 0
			for ships in shipgroups
				size++
				td = $("""<td class="stash-#{size}"></td>""")
				for ship in ships
					ship.render(td)
				tr.append(td)
			@e.find("#stash").append(tr)
		super(surface)

	add: (obj) ->
		stashed = new Stashed(obj)
		@stack[obj.color][obj.size - 1].push(stashed)
		stashed.render(@e.find(".stash-#{stashed.color} .stash-#{stashed.size}"))

	getShip: (color, size) ->
		stashed = @stack[color][size - 1].pop()
		stashed.remove()
		new Ship(stashed)

	getStar: (color, size) ->
		stashed = @stack[color][size - 1].pop()
		stashed.remove()
		new Star(stashed)


# Base class for game pieces
class Stashable extends Element

	constructor: (type) ->
		super("""
			<span class="#{type} #{@color} size-#{@size}">
			</span>
		""")

	# remove = remove from document, destroy = remove and return to stash
	destroy: () ->
		@remove()
		game.stash.add(@) # Works?


# Stashed game piece
class Stashed extends Stashable

	constructor: (current) ->
		@color = current.color
		@size = current.size
		super("stashed")


# Game piece as star
class Star extends Stashable

	constructor: (current) ->
		@color = current.color
		@size = current.size
		super("star")


# Game piece as ship
class Ship extends Stashable

	constructor: (current) ->
		@color = current.color
		@size = current.size
		super("ship")


# Solar system containing one or mutiple stars + ships of both players
class System extends Element

	constructor: (current) ->
		@pos = current.pos
		@home = current.home
		@stars = (new Star(s) for s in current.stars)
		@ships = {
			1: (new Ship(s) for s in current.ships[1]),
			2: (new Ship(s) for s in current.ships[2])
		}
		super("""
			<div class="system-clear" style="top: #{@pos[1] - 100}px; left: #{@pos[0] - 100}px;">
				<div class="system #{'system-home' if @home}">
					<div class="ships-left">
					</div>
					<div class="stars">
					</div>
					<div class="ships-right">
					</div>
				</div>
			</div>
		""")

	render: (surface) ->
		star.render(@e.find(".stars")) for star in @stars
		ship.render(@e.find(".ships-right")) for ship in @ships[1]
		ship.render(@e.find(".ships-left")) for ship in @ships[2]
		super(surface)

	addShip: (player, ship) ->
		@ships[player.id].push(ship)
		ship.render(@e.find([".ships-right", ".ships-left"][player.id - 1]))

	getShip: (player, ship) ->
		index = @ships[player.id].indexOf(ship) # not working
		ship = @ships[player.id].splice(index, 1)
		if not @ships[1] and not @ships[2]
			@destroy()
		ship.remove()
		ship

	removeStar: (star) ->
		index = @stars.indexOf(star) # not working
		@stars.splice(index, 1).destroy()
		if not stars
			@destroy()

	destroy: () ->
		@remove()
		star.destroy() for star in @stars
		ship.destroy() for ship in @ships[1]
		ship.destroy() for ship in @ships[2]


# Container for all game objects, constructor accepts current game status
class Game extends Element

	constructor: (current) ->
		@players = (new Player(p) for p in current.players)
		@systems = (new System(s) for s in current.systems)
		@stash = new Stash(current.stash)
		super("""
			<div id="game">
			</div>
		""")

	render: (surface) ->
		system.render(@e) for system in @systems
		@stash.render(@e)
		super(surface)

	toJson: () ->
		JSON.stringify(@)
