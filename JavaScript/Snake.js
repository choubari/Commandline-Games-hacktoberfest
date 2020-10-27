var snk;
var scl = 10;
var food;

function setup() {
  createCanvas(400, 400);
  snk = new snake();
  frameRate(10);
  food = createVector(floor(random(40)), floor(random(40)));
}

function draw() {
  background(112, 213, 31);

  if (snk.eat(food)) {
    var t = 0;
    do {
      t = 0;
      food.x = floor(random(40));
      food.y = floor(random(40));
      for (var i = 0; i < snk.tam; i++) {
        if (dist(food.x * scl, food.y * scl, snk.x, snk.y) < 1){
           t = 1;
        }
      }
    }while(t === 1);
  }

  snk.update();
  snk.show();
  snk.die();

  fill(200, 115, 10);
  rect(food.x * scl, food.y * scl, scl, scl);
}

function keyPressed() {
  if (keyCode === UP_ARROW && snk.vel_y != 1) {
    snk.set_d(0, -1);
  }
  if (keyCode === DOWN_ARROW && snk.vel_y != -1) {
    snk.set_d(0, 1);
  }
  if (keyCode === RIGHT_ARROW && snk.vel_x != -1) {
    snk.set_d(1, 0);
  }
  if (keyCode === LEFT_ARROW && snk.vel_x != 1) {
    snk.set_d(-1, 0);
  }

}

function snake() {
  this.x = 200;
  this.y = 200;
  this.vel_x = 0;
  this.vel_y = 0;
  this.tam = 0;
  this.tail = [];

  this.set_d = function(x, y) {
    this.vel_x = x;
    this.vel_y = y;
  }

  this.update = function() {
    if (this.tail.length === this.tam) {
      for (var i = 0; i < this.tail.length - 1; i++) {
        this.tail[i] = this.tail[i + 1];
      }
    }
    this.tail[this.tam - 1] = createVector(this.x, this.y);

    this.x = this.x + scl * this.vel_x;
    this.y = this.y + scl * this.vel_y;
    if (this.x > 400)
      this.x = 0;
    if (this.y > 400)
      this.y = 0;
    if (this.x < 0)
      this.x = 400;
    if (this.y < 0)
      this.y = 400;
  }
  this.eat = function(pos) {
    var d = dist(this.x, this.y, pos.x * scl, pos.y * scl);
    if (d < 1) {
      this.tam++;
      return true;
    } else {
      return false;
    }
  }
  this.show = function() {
    fill(200, 10, 10);
    rect(this.x, this.y, scl, scl);
    for (var i = 0; i < this.tam; i++) {
      rect(this.tail[i].x, this.tail[i].y, scl, scl);
    }
  }
  this.die = function() {
    for (var i = 0; i < this.tam; i++) {
      if (dist(this.x, this.y, this.tail[i].x, this.tail[i].y) < 1) {
        this.tail = [];
        this.tam = 0;
      }
    }
  }
}
