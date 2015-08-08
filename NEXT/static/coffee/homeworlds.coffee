#!/usr/bin/env coffee

###
Example json

{
	"systems": [
		{
			"pos": [50, 10],
			"stars": [
				{
					"color": "red",
					"size": 2
				},
				{
					"color": "yellow",
					"size": 1
				}
			],
			"ships": {
				1: [
					{
						"color": "green",
						"size": 3
					}
				],
				2: []
			}
		},
		{
			"pos": [50, 90],
			"stars": [
				{
					"color": "blue",
					"size": 1
				},
				{
					"color": "green",
					"size": 3
				}
			],
			"ships": {
				1: [],
				2: [
					{
						"color": "yellow",
						"size": 3
					}
				]
			}
		}
	],
	"players": [
		{
			"id": 1,
			"name": "Alpha",
			"actions": 1
		},
		{
			"id": 2,
			"name": "Beta",
			"actions": 0
		}
	]
}
###


class Player

	constructor: (@id, @name, @actions) ->
		@id = current.id
		@name = current.name
		@actions = current.actions

	isActive: () ->
		@actions != 0


class Element

	constructor: (e) ->
		@e = $(e)

	render: (surface) ->
		@e.detach()
		surface.append(@e)


class Stash extends Element

	constructor: (current) ->
		@stack = {
			red: ((Stashed(s) for s in current.red[i]) for i in [0..2]),
			green: ((Stashed(s) for s in current.green[i]) for i in [0..2]),
			blue: ((Stashed(s) for s in current.blue[i]) for i in [0..2]),
			yellow: ((Stashed(s) for s in current.yellow[i]) for i in [0..2])
		}
		super("""
			<div class="stash-wrapper">
				<table class="stash">
				</table>
			</div>
		""")

	render: (surface) ->
		for color, shipgroups of @stack
			tr = $("<tr></tr>")
			for ships in shipgroups
				td = $("<td></td>")
				for ship in ships :
					ship.render(td)
				tr.append(td)
			@e.find(".stash")append(tr)
		super(surface)

	add: (obj) ->
		stashed = Stashed(obj)
		@stack[obj.color][obj.size - 1] << stashed
		stashed.render(@e.find(".stash-#{stashed.color} td:nth-child(#{stashed.size})"))

	getShip: (color, size) ->
		Ship(@stack[obj.color][obj.size - 1].pop())

	getStar: (color, size) ->
		Star(@stack[obj.color][obj.size - 1].pop())


class Stashable extends Element

	constructor: (type) ->
		super("""
			<span class="#{type} color-#{@color} size-#{@size}">
			</span>
		""")

	destroy: () ->
		game.stash.add(@)


class Stashed extends Stashable

	constructor: (current) ->
		@color = current.color
		@size = current.size
		super("stashed")


class Star extends Stashable

	constructor: (current) ->
		@color = current.color
		@size = current.size
		super("star")


class Ship extends Stashable

	constructor: (current) ->
		@color = current.color
		@size = current.size
		super("ship")


class System extends Element

	constructor: (current) ->
		@pos = current.pos
		@stars = (Star(s) for s in current.stars)
		@ships = {
			1: (Ship(s) for s in current.ships[1]),
			2: (Ship(s) for s in current.ships[2])
		}
		super("""
			<div class="system-clear">
				<div class="system" style="top: #{@pos[1]}; left: #{@pos[0]};">
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
		@ships[player.id] << ship
		ship.render(@e.find(".ships-right" if player.id == 1 else ".ships-left"))

	getShip: (player, ship) ->
		index = @ships[player.id].indexOf(ship)
		ship = @ships[player.id].splice(index, 1)
		if not ships[1] and not ships[2]
			@destroy()
		ship

	removeStar: (player, star) ->
		index = @stars.indexOf(star)
		@stars.splice(index, 1).destroy()
		if not stars
			@destroy()

	destroy: () ->
		star.destroy() for star in @stars
		ship.destroy() for ship in @ships[1]
		ship.destroy() for ship in @ships[2]


class Game extends Element

	constructor: (current) ->
		@players = (Player(p) for p in current.players)
		@systems = (System(s) for s in current.systems)
		@stash = Stash(current.stash)
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
