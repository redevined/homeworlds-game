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
			"ships_p1": [
				{
					"color": "green",
					"size": 3
				}
			],
			"ships_p2": [
			]
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
			"ships_p1": [
			],
			"ships_p2": [
				{
					"color": "yellow",
					"size": 3
				}
			]
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


class Element

	constructor: (e) ->
		@e = $(e)

	destroy: () ->
		@e.remove()

	render: (surface) ->
		surface.append(@e)


class System extends Element

	constructor: (@pos, @stars, ships_p1, ships_p2) ->
		@ships = {
			1: ships_p1,
			2: ships_p2
		}
		super("""
			<div class="system-clear">
				<div class="system" style="top: #{@pos[1]}; left: #{@pos[0]};">
					<div class="ships_p2">
						<!-- Player 2 ships -->
					</div>
					<div class="stars">
						<!-- Stars -->
					</div>
					<div class="ships_p1">
						<!-- Player 1 ships -->
					</div>
				</div>
			</div>
		""")

	destroy: () ->
		star.destroy() for star in @stars
		ship.destroy() for ship in @ships[1]
		ship.destroy() for ship in @ships[2]
		super()

	render: (surface) ->
		star.render(@e.find(".stars")) for star in @stars
		ship.render(@e.find(".ships_p1")) for ship in @ships[1]
		ship.render(@e.find(".ships_p2")) for ship in @ships[2]
		super(surface)

	addShip: (player, ship) ->
		@ships[player.id] << ship

	removeShip: (player, ship) ->
		index = @ships[player.id].indexOf(ship)
		if index != -1
			@ships[player.id].splice(index, 1).destroy()
		if not ships[1] and not ships[2]
			@destroy()

	removeStar: (star) ->
		index = @stars.indexOf(ship)
		if index != -1
			@stars.splice(index, 1).destroy()
		if not stars
			@destroy()
