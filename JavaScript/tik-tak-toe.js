var readline = require('readline');

var rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});


// getting the input
function getPrompt(symbol) {
  return `Ssi (${symbol} ), golina fin ghiti t7et sign dyalk: `;
}

// check if a player can move
function canMakeMove(board, location) {

  if (location === board[location]) {
    return true;
  }
  return false;
}

// checking the game state
function checkGame(board, counter) {

  function noWinner() {
    return counter < 9 ? false : true;
  }

  var winner;
  function checkForWinningStreak(board, triad) {

    if (board[triad[0]] === board[triad[1]]) {
      if (board[triad[1]] === board[triad[2]]) {
        winner = board[triad[0]];
        return true;
      }
    }
    return false;
  }

  function winPos() {
    var winPositions = [['p11','p21','p31'], ['p12','p22','p32'], ['p13','p23','p33'],
                  ['p11','p12','p13'], ['p21','p22','p23'], ['p31','p32','p33'],
                  ['p11','p22','p33'], ['p31','p22','p13']];

    var matches = winPositions.filter(function(triad) {
      return checkForWinningStreak(board, triad);
    });
    return matches.length > 0;
  }

  if (winPos()) {
    return 'Ssi ' + winner + 'n3ad 3tak selkha mo3tabara'  ;
  } else if (noWinner()) {
    return 'Sorry but you both suck';
  } else {
    return false;
  }
}

// Changing the player
function togglePlayer(player) {
  if (player === '1') {
    return '2';
  }
  return '1';
}

// let's play boizzz
function play() {

  var board = {
    p11: 'p11', p12: 'p12', p13: 'p13',
    p21: 'p21', p22: 'p22', p23: 'p23',
    p31: 'p31', p32: 'p32', p33: 'p33'
  };
  var playerMap = {'1': 'X', '2': 'O'};
  var currentPlayer = '1';
  var counter = 0;


  showBoard(board);
  rl.setPrompt(getPrompt(currentPlayer, playerMap[currentPlayer]));
  rl.prompt();


  function afterMoves() {

    counter ++;
    showBoard(board);

    var gameStatus = checkGame(board, counter);

    if (gameStatus) {
      console.log('Salina l 7afla ', gameStatus);
      rl.close();

      return false;

    } else {
      currentPlayer = togglePlayer(currentPlayer);

      rl.setPrompt(getPrompt(currentPlayer, playerMap[currentPlayer]));
      rl.prompt();

      return true;
    }
  }

  // showing the board
  function showBoard(board) {

    console.log(`
      ${board.p11} | ${board.p12} | ${board.p13}
      ___ ____ ___\n
      ${board.p21} | ${board.p22} | ${board.p23}
      ___ ____ ___\n
      ${board.p31} | ${board.p32} | ${board.p33}
    `);
  }
  
  rl.on('line', function(input) {

    if (canMakeMove(board, input)) {
      board[input] = playerMap[currentPlayer];
      afterMoves();
    } else {
      showBoard(board);
      console.log('Wach rak t3mel a sa7bi !!! zyer m3ana w 3awd');
    }
  });
}

play();
