/*
This program will prompts to the user to select either Rock, Paper, Scissors, Lizard or Spock.
The computer will randomly select each of them.
Then compares the choices and inform who the winner is.
The rules are the following:
scissors cut paper,
paper covers rock,
rock crushes lizard,
lizard poisens Spock,
Spock smashes scissors,
scissors decapotates lizard,
lizard eats paper,
paper disproves Spock,
Spock vaporises rock,
and as it always has,
rock crushes scissors.
*/

#include <iostream>
#include <stdlib.h>

int main() {
  //Chance random number every execution
  srand(time(NULL));
  //Computer's choice from 1-5
  int computer = rand() %5 +1;
  //User's choice 
  int user=0;
  //The result of the game
  std::string result;
  //Rule applued to that case
  std::string rule;

  std::cout << "=================================\n";
  std::cout << "rock paper scissors Lizard Spock!\n";
  std::cout << "=================================\n";

  std::cout << "1) rock\n";
  std::cout << "2) paper\n";
  std::cout << "3) scissors\n";
  std::cout << "4) lizard\n";
  std::cout << "5) spock\n";
  std::cin >> user;

  if (user == 1){

    /*   ROCK   */
    if (computer == 1){
      result = "Tie!";
      rule = "Same choice";
    } else if (computer == 2){
      result = "Lose!";
      rule = "paper covers rock";
    } else if (computer == 3) {
      result = "Win!";
      rule = "rock crushes scissors";
    } else if (computer == 4) {
      result = "Win!";
      rule = "rock crushes lizard";
    } else if (computer == 5) {
      result = "Lose!";
      rule = "Spock vaporises rock";
    }
    /*   ROCK   */

  } else if (user == 2){

    /*   PAPER   */
    if (computer == 1){
      result = "Win!";
      rule = "paper covers rock";
    } else if (computer == 2){
      result = "Tie!";
      rule = "Same choice";
    } else if (computer == 3)  {
      result = "Lose!";
      rule = "scissors cut paper";
    } else if (computer == 4) {
      result = "Lose!";
      rule = "lizard eats paper";
    } else if (computer == 5) {
      result = "Win!";
      rule = "paper disproves Spock";
    }
    /*   PAPER   */

  } else if (user == 3) {

    /*   SCISSORS   */
    if (computer == 1){
      result = "Lose!";
      rule = "rock crushes scissors";
    } else if (computer == 2){
      result = "Win!";
      rule = "scissors cut paper";
    } else if (computer == 3) {
      result = "Tie!";
      rule = "Same choice";
    } else if (computer == 4) {
      result = "Win!";
      rule = "scissors decapotates lizard";
    } else if (computer == 5) {
      result = "Lose!";
      rule = "Spock smashes scissors";
    }
    /*   SCISSORS   */

  } else if (user == 4){

    /*   LIZARD   */
    if (computer == 1){
      result = "Lose!";
      rule = "rock crushes lizard";
    } else if (computer == 2){
      result = "Win!";
      rule = "lizard eats paper";
    } else if (computer == 3) {
      result = "Lose!";
      rule = "scissors decapotates lizard";
    } else if (computer == 4) {
      result = "Tie!";
      rule = "Same choice";
    } else if (computer == 5) {
      result = "Win!";
      rule = "lizard poisens Spock";
    }
    /*   LIZARD   */

  } else if (user == 5){

    /*   SPOCK   */
    if (computer == 1){
      result = "Win!";
      rule = "Spock vaporises rock";
    } else if (computer == 2){
      result = "Lose!";
      rule = "paper disproves Spock";
    } else if (computer == 3) {
      result = "Win!";
      rule = "Spock smashes scissors";
    } else if (computer == 4) {
      result = "Lose!";
      rule = "lizard poisens Spock";
    } else if (computer == 5) {
      result = "Tie!";
      rule = "Same choice";
    }
    /*   SPOCK   */

  }

  std::cout << result << "\n";
  std::cout << rule << ".\n";

  return 0;
}

