import java.util.Scanner;

public class TicTacToeGame {
  private char positions[];
  private char player;
  //Colors
  static final String COLOR_RESET = "\033[0m";
  // Regular Colors
  static final String COLOR_RED = "\033[31m";
  static final String COLOR_GREEN = "\033[32m";

  TicTacToeGame() {
    positions = new char[10];
  }

  // -----------initializing board--------------
  public void initboard() {
    char init[] = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' };
    player = 'X';
    for (int i = 1; i < 10; i++) {
      positions[i] = init[i];
    }
  }

  // -------------showing board-----------
  public void showboard() {
    int position = 1;    
    System.out.println(addColorSymbols("\n\t _________________\n"));
    for (int i = 0 ; i < 3; i++) {
      System.out.print("\t");
      for (int j = 0; j < 3; j++) {
        System.out.print(addColorSymbols("|  "));
        System.out.print(positions[position]);
        System.out.print(addColorSymbols("  "));
        position++;
      }
      System.out.println(addColorSymbols("\n\t _________________\n"));
    }
  }

  // ------------get Player name (X or O)------------
  public char getPlayer() {
    return player;
  }

  // -----------next Player symbol---------------
  public void nextPlayer() {
    if (player == 'X') {
      player = 'O';
    } else {
      player = 'X';
    }
  }

  // -------------checkPosition----------------
  public boolean checkPosition(int spot) {
    if (positions[spot] == 'X' || positions[spot] == 'O') {
      legendDisplay("----> The position is already taken, Please choose an other number");
      return true;
    } else {
      return false;
    }
  }

  // ----------------check who's the Winner-------------------
  public char checkWinner() {
    char[] winer = { 'X', 'O' };
    char theWinnerIs = ' ';
    for (int i = 0; i < 2; i++) {
      if (positions[1] == winer[i] && positions[2] == winer[i] && positions[3] == winer[i]) {
        theWinnerIs = winer[i];
        break;
      }
      if (positions[4] == winer[i] && positions[5] == winer[i] && positions[6] == winer[i]) {
        theWinnerIs = winer[i];
        break;
      }
      if (positions[7] == winer[i] && positions[8] == winer[i] && positions[9] == winer[i]) {
        theWinnerIs = winer[i];
        break;
      }
      if (positions[1] == winer[i] && positions[4] == winer[i] && positions[7] == winer[i]) {
        theWinnerIs = winer[i];
        break;
      }
      if (positions[2] == winer[i] && positions[5] == winer[i] && positions[8] == winer[i]) {
        theWinnerIs = winer[i];
        break;
      }
      if (positions[3] == winer[i] && positions[6] == winer[i] && positions[9] == winer[i]) {
        theWinnerIs = winer[i];
        break;
      }
      if (positions[1] == winer[i] && positions[5] == winer[i] && positions[9] == winer[i]) {
        theWinnerIs = winer[i];
        break;
      }
      if (positions[3] == winer[i] && positions[5] == winer[i] && positions[7] == winer[i]) {
        theWinnerIs = winer[i];
        break;
      }
    }

    if (theWinnerIs == 'X' || theWinnerIs == 'O') {
      legendDisplay("<<--The Player with " + blink(theWinnerIs + "") + COLOR_RED + " wins-->>");
      return theWinnerIs;
    }

    for (int i = 1; i < 10; i++) {
      if (positions[i] == 'X' || positions[i] == 'O') {
        if (i == 9) {
          char Draw = 'D';
          legendDisplay(" <<--Draw !-->> ");
          return Draw;
        }
      } else {
        break;
      }
    }
    return theWinnerIs;
  }

  // -------------managing the process of playing -----------------
  public void play() {
    int spot;
    char blank = ' ';
    do {
      showboard();
      legendDisplay("\n\n ----> Player " + blink(getPlayer() + "") + COLOR_GREEN + ", Please choose a position: ");
      boolean positionTaken = true;
      while (positionTaken) {
        Scanner in = new Scanner(System.in);
        spot = in.nextInt();
        positionTaken = checkPosition(spot);
        if (positionTaken == false)
          positions[spot] = getPlayer();
      }
      clearDisplay();
      nextPlayer();
    } while (checkWinner() == blank);
    showboard();
  }

  /**
   * Return color
   */
  private String addColorSymbols(final String symbol) {
    return COLOR_GREEN + symbol + COLOR_RESET;
  }

  /**
   * Return efect blink for GUI
   */
  private String blink(final String element) {
    return "\033[5m" + element + "\033[0m";
  }

  /**
   * Clear console
   */
  public void clearDisplay() {
    System.out.println("\033[2J\033[1;1H");
  }

  /**
   * Print message color green
   */
  public void legendDisplay(final String text) {
    System.out.println(COLOR_GREEN + text);
  }
}
