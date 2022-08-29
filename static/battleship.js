function squircle(i, j, size, radius=0.25, padding=0.2, stroke_weight=0.02) {
  strokeWeight(size * stroke_weight);
  square(size * (i + padding / 2), size * (j + padding / 2), size - size * padding, size * radius);
};

function X(i, j, size, padding=0.2, stroke_weight=0.08) {
  strokeWeight(size * stroke_weight);
  line(size * (i + padding / 2), size * (j + padding / 2), size * (i + 1 - padding / 2), size * (j + 1 - padding / 2));
  line(size * (i + padding / 2), size * (j + 1 - padding / 2), size * (i + 1 - padding / 2), size * (j + padding / 2));
}

colors = [
  '#C9D5B5',
  '#3C6E71',
  '#284B63',
  '#C83E4D',
  '#F39237',
]


function ship(i, j, size, selected) {
  if (selected) {
    stroke(colors[0]);
    fill(colors[1]);
  } else {
    stroke(colors[0]);
    fill(colors[0]);
  }
  squircle(i, j, size, 0.3);
}

function sunk(i, j, size) {
  stroke(colors[0]);
  fill(colors[3]);
  squircle(i, j, size, 0.2);
}

function hit(i, j, size) {
  stroke(colors[0]);
  fill(colors[4]);
  squircle(i, j, size, 0.2);
}

function miss(i, j, size) {
  stroke(colors[0]);
  fill(colors[0]);
  X(i, j, size, 0.4);
}

function hovering(i, j, size) {
  stroke(colors[0]);
  fill(colors[1]);
  squircle(i, j, size, 0.25, 0);
}

function selector(i, j, size) {
  stroke(colors[0]);
  fill(colors[1]);
  squircle(i, j, size);
}

function transparent_selector(i, j, size) {
  stroke(colors[0] + '80');
  fill(colors[1] + '80');
  squircle(i, j, size);
}

function cell(i, j, size) {
  stroke(colors[0]);
  fill(colors[2]);
  squircle(i, j, size, 0.25, 0);
}

var alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

function grid(x, y, size) {
  textSize(size / 2);
  for (let i = 0; i < x; i++) {
    stroke(colors[0]);
    fill(colors[0]);
    textAlign(CENTER, BOTTOM);
    text(alphabet[i], size * (i + 1/2), -size/4);
    for (let j = 0; j < y; j++) {
      if (i == 0) {
        stroke(colors[0]);
        fill(colors[0]);
        textAlign(RIGHT, CENTER);
        text(j + 1, -size/4, size * (j + 1/2));
      }
      cell(i, j, size);
    }
  }
}

class Ship {
  constructor(shape, name) {
    this.shape = shape.map(function(arr) {
      return arr.slice();
    });
    this.name = name;
    this.x = null;
    this.y = null;
    this.moving = false;
    this.selected = false;
  };
  rotate() {
    let new_shape = [];
    for (let i=this.shape[0].length - 1; i>=0; i--) {
      let row = [];
      for (let j=0; j<this.shape.length; j++) {
        row.push(this.shape[j][i]);
      };
      new_shape.push(row);
    };
    this.shape = new_shape;
  };
  flip_vertically() {
    let new_shape = [];
    for (let i=this.shape.length - 1; i>=0; i--) {
      let row = [];
      for (let j=0; j<this.shape[0].length; j++) {
        row.push(this.shape[i][j]);
      };
      new_shape.push(row);
    };
    this.shape = new_shape;
  };
  flip_horizontally() {
    let new_shape = [];
    for (let i=0; i<this.shape.length; i++) {
      let row = [];
      for (let j=this.shape[0].length - 1; j>=0; j--) {
        row.push(this.shape[i][j]);
      };
      new_shape.push(row);
    };
    this.shape = new_shape;
  };
  transform(string) {
    for (let i of string) {
      if (i == 'R') {
        this.rotate();
      } else if (i == 'V') {
        this.flip_vertically();
      } else if (i == 'H') {
        this.flip_horizontally();
      }
    };
  };
  copy() {
    let ship = new Ship(this.shape, this.name);
    ship.x = this.x;
    ship.y = this.y;
    return ship;
  };
  to_json() {
    return {
      name: this.name,
      x: this.x,
      y: this.y,
      shape: this.shape
    };
  };
  static from_json(json) {
    let ship = new Ship(json.shape, json.name);
    ship.x = json.x;
    ship.y = json.y;
    return ship;
  };
  draw(size) {
    if (this.moving) return;
    for (let i=0; i<this.shape.length; i++) {
      for (let j=0; j<this.shape[0].length; j++) {
        if (this.shape[i][j]) {
          ship(this.y + j, this.x + i, size, this.selected);
        }
      }
    }
  }
  draw_hovering(size) {
    for (let i=0; i<this.shape.length; i++) {
      for (let j=0; j<this.shape[0].length; j++) {
        if (this.shape[i][j]) {
          hovering(this.y + j, this.x + i, size);
        }
      }
    }
  }
  is_on_cell(x, y) {
    let i = y - this.x;
    let j = x - this.y;
    if (i < 0 || i >= this.shape.length || j < 0 || j >= this.shape[0].length) {
      return false;
    }
    return this.shape[i][j];
  };
};


var ship_1x2 = new Ship([
  [1,1],
], '1x2');
var ship_1x3 = new Ship([
  [1,1,1],
], '1x3');
var ship_1x4 = new Ship([
  [1,1,1,1],
], '1x4');
var ship_1x5 = new Ship([
  [1,1,1,1,1],
], '1x5');
var ship_lightning = new Ship([
  [1,1,0],
  [0,1,1],
], 'lightning');
var ship_small_l = new Ship([
  [1,0],
  [1,1],
], 'small_l');
var ship_large_l = new Ship([
  [1,0,0],
  [1,0,0],
  [1,1,1],
], 'large_l');
var ship_long_l = new Ship([
  [1,0,0,0],
  [1,1,1,1],
], 'long_l');
var ship_small_t = new Ship([
  [1,1,1],
  [0,1,0],
], 'small_t');
var ship_large_t = new Ship([
  [1,1,1],
  [0,1,0],
  [0,1,0],
], 'large_t');

var ships_dict = {
  '1x2': ship_1x2,
  '1x3': ship_1x3,
  '1x4': ship_1x4,
  '1x5': ship_1x5,
  'lightning': ship_lightning,
  'small_l': ship_small_l,
  'large_l': ship_large_l,
  'long_l': ship_long_l,
  'small_t': ship_small_t,
  'large_t': ship_large_t,
};


class Board {
  constructor(size, ships, board) {
    this.size = size;
    this.ships = ships;
    this.board = board;
  };
  to_json() {
    return {
      size: this.size,
      ships: this.ships,
      board: this.board
    };
  };
  static from_json(json) {
    let ships = [];
    for (let ship of json.ships) {
      ships.push(Ship.from_json(ship));
    };
    return new Board(json.size, ships, json.board);
  };
  draw(size) {
    for (var ship of this.ships) {
      ship.draw(size);
    };
  };
  draw_board(size) {
    for (var i=0; i < this.size[0]; i++) {
      for (var j=0; j < this.size[1]; j++) {
        if (this.board[i][j] == 1) {
          ship(j, i, size, false);
        } else if (this.board[i][j] == 2) {
          hit(j, i, size);
        } else if (this.board[i][j] == 3) {
          miss(j, i, size);
        } else if (this.board[i][j] == 4) {
          sunk(j, i, size);
        }
      }
    }
  }
};


class ShotBoard {
  constructor(size, shots) {
    this.size = size;
    this.shots = shots;
  };
  to_json() {
    return {
      size: this.size,
      shots: this.shots
    };
  };
  static from_json(json) {
    return new ShotBoard(json.size, json.shots);
  };
  draw_board(size) {
    for (var i=0; i < this.size[0]; i++) {
      for (var j=0; j < this.size[1]; j++) {
        if (this.shots[i][j] == 1) {
          ship(j, i, size, false);
        } else if (this.shots[i][j] == 2) {
          hit(j, i, size);
        } else if (this.shots[i][j] == 3) {
          miss(j, i, size);
        } else if (this.shots[i][j] == 4) {
          sunk(j, i, size);
        }
      }
    }
  }
};

