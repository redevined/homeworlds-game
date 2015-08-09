var Element, Game, Player, Ship, Star, Stash, Stashable, Stashed, System,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

Player = (function() {
  function Player(id, name, actions) {
    this.id = id;
    this.name = name;
    this.actions = actions;
    this.id = current.id;
    this.name = current.name;
    this.actions = current.actions;
  }

  Player.prototype.isActive = function() {
    return this.actions !== 0;
  };

  return Player;

})();

Element = (function() {
  function Element(e) {
    this.e = $(e);
  }

  Element.prototype.render = function(surface) {
    this.e.detach();
    return surface.append(this.e);
  };

  return Element;

})();

Stash = (function(superClass) {
  extend(Stash, superClass);

  function Stash(current) {
    var i, s;
    this.stack = {
      red: (function() {
        var j, results;
        results = [];
        for (i = j = 0; j <= 2; i = ++j) {
          results.push((function() {
            var k, len, ref, results1;
            ref = current.red[i];
            results1 = [];
            for (k = 0, len = ref.length; k < len; k++) {
              s = ref[k];
              results1.push(Stashed(s));
            }
            return results1;
          })());
        }
        return results;
      })(),
      green: (function() {
        var j, results;
        results = [];
        for (i = j = 0; j <= 2; i = ++j) {
          results.push((function() {
            var k, len, ref, results1;
            ref = current.green[i];
            results1 = [];
            for (k = 0, len = ref.length; k < len; k++) {
              s = ref[k];
              results1.push(Stashed(s));
            }
            return results1;
          })());
        }
        return results;
      })(),
      blue: (function() {
        var j, results;
        results = [];
        for (i = j = 0; j <= 2; i = ++j) {
          results.push((function() {
            var k, len, ref, results1;
            ref = current.blue[i];
            results1 = [];
            for (k = 0, len = ref.length; k < len; k++) {
              s = ref[k];
              results1.push(Stashed(s));
            }
            return results1;
          })());
        }
        return results;
      })(),
      yellow: (function() {
        var j, results;
        results = [];
        for (i = j = 0; j <= 2; i = ++j) {
          results.push((function() {
            var k, len, ref, results1;
            ref = current.yellow[i];
            results1 = [];
            for (k = 0, len = ref.length; k < len; k++) {
              s = ref[k];
              results1.push(Stashed(s));
            }
            return results1;
          })());
        }
        return results;
      })()
    };
    Stash.__super__.constructor.call(this, "<div class=\"stash-wrapper\">\n	<table class=\"stash\">\n	</table>\n</div>");
  }

  Stash.prototype.render = function(surface) {
    var color, j, k, len, len1, ref, ship, shipgroups, ships, td, tr;
    ref = this.stack;
    for (color in ref) {
      shipgroups = ref[color];
      tr = $("<tr></tr>");
      for (j = 0, len = shipgroups.length; j < len; j++) {
        ships = shipgroups[j];
        td = $("<td></td>");
        for (k = 0, len1 = ships.length; k < len1; k++) {
          ship = ships[k];
          ship.render(td);
        }
        tr.append(td);
      }
      this.e.find(".stash").append(tr);
    }
    return Stash.__super__.render.call(this, surface);
  };

  Stash.prototype.add = function(obj) {
    var stashed;
    stashed = Stashed(obj);
    this.stack[obj.color][obj.size - 1] << stashed;
    return stashed.render(this.e.find(".stash-" + stashed.color + " td:nth-child(" + stashed.size + ")"));
  };

  Stash.prototype.getShip = function(color, size) {
    return Ship(this.stack[obj.color][obj.size - 1].pop());
  };

  Stash.prototype.getStar = function(color, size) {
    return Star(this.stack[obj.color][obj.size - 1].pop());
  };

  return Stash;

})(Element);

Stashable = (function(superClass) {
  extend(Stashable, superClass);

  function Stashable(type) {
    Stashable.__super__.constructor.call(this, "<span class=\"" + type + " color-" + this.color + " size-" + this.size + "\">\n</span>");
  }

  Stashable.prototype.destroy = function() {
    return game.stash.add(this);
  };

  return Stashable;

})(Element);

Stashed = (function(superClass) {
  extend(Stashed, superClass);

  function Stashed(current) {
    this.color = current.color;
    this.size = current.size;
    Stashed.__super__.constructor.call(this, "stashed");
  }

  return Stashed;

})(Stashable);

Star = (function(superClass) {
  extend(Star, superClass);

  function Star(current) {
    this.color = current.color;
    this.size = current.size;
    Star.__super__.constructor.call(this, "star");
  }

  return Star;

})(Stashable);

Ship = (function(superClass) {
  extend(Ship, superClass);

  function Ship(current) {
    this.color = current.color;
    this.size = current.size;
    Ship.__super__.constructor.call(this, "ship");
  }

  return Ship;

})(Stashable);

System = (function(superClass) {
  extend(System, superClass);

  function System(current) {
    var s;
    this.pos = current.pos;
    this.stars = (function() {
      var j, len, ref, results;
      ref = current.stars;
      results = [];
      for (j = 0, len = ref.length; j < len; j++) {
        s = ref[j];
        results.push(Star(s));
      }
      return results;
    })();
    this.ships = {
      1: (function() {
        var j, len, ref, results;
        ref = current.ships[1];
        results = [];
        for (j = 0, len = ref.length; j < len; j++) {
          s = ref[j];
          results.push(Ship(s));
        }
        return results;
      })(),
      2: (function() {
        var j, len, ref, results;
        ref = current.ships[2];
        results = [];
        for (j = 0, len = ref.length; j < len; j++) {
          s = ref[j];
          results.push(Ship(s));
        }
        return results;
      })()
    };
    System.__super__.constructor.call(this, "<div class=\"system-clear\">\n	<div class=\"system\" style=\"top: " + (this.pos[1] - 100) + "; left: " + (this.pos[0] - 100) + ";\">\n		<div class=\"ships-left\">\n		</div>\n		<div class=\"stars\">\n		</div>\n		<div class=\"ships-right\">\n		</div>\n	</div>\n</div>");
  }

  System.prototype.render = function(surface) {
    var j, k, l, len, len1, len2, ref, ref1, ref2, ship, star;
    ref = this.stars;
    for (j = 0, len = ref.length; j < len; j++) {
      star = ref[j];
      star.render(this.e.find(".stars"));
    }
    ref1 = this.ships[1];
    for (k = 0, len1 = ref1.length; k < len1; k++) {
      ship = ref1[k];
      ship.render(this.e.find(".ships-right"));
    }
    ref2 = this.ships[2];
    for (l = 0, len2 = ref2.length; l < len2; l++) {
      ship = ref2[l];
      ship.render(this.e.find(".ships-left"));
    }
    return System.__super__.render.call(this, surface);
  };

  System.prototype.addShip = function(player, ship) {
    this.ships[player.id] << ship;
    return ship.render(this.e.find(player.id === 1 ? ".ships-right" : ".ships-left"));
  };

  System.prototype.getShip = function(player, ship) {
    var index;
    index = this.ships[player.id].indexOf(ship);
    ship = this.ships[player.id].splice(index, 1);
    if (!ships[1] && !ships[2]) {
      this.destroy();
    }
    return ship;
  };

  System.prototype.removeStar = function(player, star) {
    var index;
    index = this.stars.indexOf(star);
    this.stars.splice(index, 1).destroy();
    if (!stars) {
      return this.destroy();
    }
  };

  System.prototype.destroy = function() {
    var j, k, l, len, len1, len2, ref, ref1, ref2, results, ship, star;
    ref = this.stars;
    for (j = 0, len = ref.length; j < len; j++) {
      star = ref[j];
      star.destroy();
    }
    ref1 = this.ships[1];
    for (k = 0, len1 = ref1.length; k < len1; k++) {
      ship = ref1[k];
      ship.destroy();
    }
    ref2 = this.ships[2];
    results = [];
    for (l = 0, len2 = ref2.length; l < len2; l++) {
      ship = ref2[l];
      results.push(ship.destroy());
    }
    return results;
  };

  return System;

})(Element);

Game = (function(superClass) {
  extend(Game, superClass);

  function Game(current) {
    var p, s;
    this.players = (function() {
      var j, len, ref, results;
      ref = current.players;
      results = [];
      for (j = 0, len = ref.length; j < len; j++) {
        p = ref[j];
        results.push(Player(p));
      }
      return results;
    })();
    this.systems = (function() {
      var j, len, ref, results;
      ref = current.systems;
      results = [];
      for (j = 0, len = ref.length; j < len; j++) {
        s = ref[j];
        results.push(System(s));
      }
      return results;
    })();
    this.stash = Stash(current.stash);
    Game.__super__.constructor.call(this, "<div id=\"game\">\n</div>");
  }

  Game.prototype.render = function(surface) {
    var j, len, ref, system;
    ref = this.systems;
    for (j = 0, len = ref.length; j < len; j++) {
      system = ref[j];
      system.render(this.e);
    }
    this.stash.render(this.e);
    return Game.__super__.render.call(this, surface);
  };

  Game.prototype.toJson = function() {
    return JSON.stringify(this);
  };

  return Game;

})(Element);
