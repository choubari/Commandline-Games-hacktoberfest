#include <bits/stdc++.h>
#include <cstdlib>
#include <ctime>

using namespace std;


void play();
void ReviewStat();
int Roll();

// dice rolling function
int Roll() {
   int die1;
   int die2;
   int workSum;
   
   die1 = 1 + rand() % 6;
   die2 = 1 + rand() % 6;

   workSum = die1 + die2;
   cout << "Player rolled " << die1 << " + " << die2
        << " = " << workSum << endl;
        
   return workSum;
}

// play game function
void play() {
    enum Status { CONTINUE, WON, LOST };
    int sum; 
    int myPoint;
    int rollCount = 0;
    Status gameStatus;
    
    srand( time( 0 ) );
    sum = Roll();
    rollCount++;
    
    switch( sum ) {
        case 7:
        case 11:
            gameStatus = WON;
            break;
        case 2:
        case 3:
        case 12:
            gameStatus = LOST;
            break;
        default:
            gameStatus = CONTINUE;
            myPoint = sum;
            cout << "Point is " << myPoint << endl;
            break;

   }
   
   while ( gameStatus == CONTINUE ) { 
        sum = Roll();
        rollCount++;
        
        if ( sum == myPoint )
            gameStatus = WON;

        else
            if ( sum == 7 )
                gameStatus = LOST;

   }
    if ( gameStatus == WON ) {
        cout << "Player wins\n" << endl;           
    } 
    else {
        cout << "Player loses\n" << endl;
    } 

}

int main() {
    int choice;
    do {
        cout << "Choose an option" << endl
            << "1. Play the game" << endl
            << "2. Quit" << endl;
        cin >> choice;
        if ( choice == 1 )
            play();
    } while ( choice != 2 );
    return 0;
} 