#include <iostream>
#include <cstdlib>
#include "ufo_functions.h"

int main() {

  //Game title
  greet();

  //List of codewords
  std::vector<std::string> codeword_list = {"humans","peace","extraterrestrial","aliens"};

  //Set the random number
  srand(time(NULL));

  //Get random index
  int index = rand() % codeword_list.size();

  //Codeword the player try to guess
  std::string codeword= codeword_list[index];
  //Stores correctly guessed letters with blanks in between
  std::string answer= "";
  for (int i=0;i<codeword_list[index].size();i++){
    answer += "_";
  }  
  //Number of missed letters
  int misses=0;
  //List of incorrect letters entered
  std::vector<char> incorrect;
  //This variable tracks wheter the player guessed a correct letter
  bool guess=false;
  //Player's guessed letter
  char letter;

  //Game loop
  while (answer!=codeword && misses<7){

    //Player's abduction status
    display_misses(misses);
    display_status(incorrect,answer);

    //Get user input
    std::cout << "Please enter your guess: ";
    std::cin >> letter;
    
    //Search for that letter
    for (int i=0;i<codeword.size();i++){

      if (letter==codeword[i]){
        answer[i]=letter;
        guess=true;
      }
    }

    //Check if it has been found
    if (guess){
      std::cout << "Correct!\n";
    } else {
      std::cout << "Incorrect! The tractor beam pulls the person in further.\n";
      //Add to the list of incorrect letters
      incorrect.push_back(letter);
      //Add counter
      misses++;
    }

    //Reset guess for the next iteration
    guess=false;

  }

  //Game result
  endgame(answer,codeword);

}
