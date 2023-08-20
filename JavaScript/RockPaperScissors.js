const choices = ["rock", "paper", "scissors"];

const userInput = prompt("Do you choose rock, paper or scissors?");
if (userInput === "paper" || userInput === "rock" || userInput === "scissors") {
  console.log("You chose " + `${userInput}`);
} else {
  console.log("Error! Try again!");
}

let computerInput = choices[Math.floor(Math.random() * 3)];
console.log("Computer chose" + ` ${computerInput}`);

const winner = declareWinner(userInput, computerInput);

function declareWinner(userInput, computerInput) {
  switch (userInput) {
    
    case "rock":
      switch (computerInput) {
        case "paper":
          console.log("You lose! Paper beats Rock");
          break;
        case "scissors":
          console.log("You win! Rock beats Scissors");
          break;
        default:
          console.log("You tie!");
          break;
      }
      break;

      case "paper":
      switch (computerInput) {
        case "rock":
          console.log("You win! Paper beats Rock");
          break;
        case "scissors":
          console.log("You lose! Scissors beats Paper");
          break;
        default:
          console.log("You tie!");
          break;
      }
      break;

      case "scissors":
      switch (computerInput) {
        case "rock":
          console.log("You lose! Rock beats Scissors");
          break;
        case "paper":
          console.log("You win! Scissors beats Paper");
          break;
        default:
          console.log("You tie!");
          break;
      }
      break;
  }
}
