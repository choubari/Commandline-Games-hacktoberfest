import java.util.*;
public class TicTacToeGame {
	private   char positions[]=new char[10];
	char player;
	//-----------initializing board--------------
	public void  initboard() {
		char init[] = {'0','1', '2', '3', '4', '5', '6', '7', '8', '9'};
		player = 'X';
		for (int i=1; i<10; i++)
			positions[i]=init[i];
	}
	//-------------showing board-----------
	public void showboard() {
		System.out.println("\n\t _________________ \n");
		System.out.println("\t|  "+positions[1]+"  |  "+positions[2]+"  |  "+positions[3]+"  |\n");
		System.out.println("\t|_________________|\n");
		System.out.println("\t|  "+positions[4]+"  |  "+positions[5]+"  |  "+positions[6]+"  |\n");
		System.out.println("\t|_________________|\n");
		System.out.println("\t|  "+positions[7]+"  |  "+positions[8]+"  |  "+positions[9]+"  |\n");
		System.out.println("\t|_________________|\n");
	}
	//------------get Player name (X or O)------------
	public  char getPlayer(){
        return player;
    }
	//-----------next Player symbol---------------
	 public  void nextPlayer(){
	    if (player == 'X')
	    	player = 'O';
	    else player = 'X';    
	 }  
	 //-------------checkPosition----------------
	 public  boolean checkPosition(int spot){
	        if (positions[spot] == 'X' || positions[spot] == 'O'){
	            System.out.println("----> The position is already taken, Please choose an other number");
	            return true;
	        }
	        else {
	            return false;
	        }
	 }
	//----------------check who's the Winner-------------------
	public  char checkWinner(){
        char TheWinnerIs = ' ';	        
	        // Check if X is the winner
	        if (positions[1] == 'X' && positions[2] == 'X' && positions[3] == 'X') TheWinnerIs = 'X';
	        if (positions[4] == 'X' && positions[5] == 'X' && positions[6] == 'X') TheWinnerIs = 'X';
	        if (positions[7] == 'X' && positions[8] == 'X' && positions[9] == 'X') TheWinnerIs = 'X';
	        if (positions[1] == 'X' && positions[4] == 'X' && positions[7] == 'X') TheWinnerIs = 'X';
	        if (positions[2] == 'X' && positions[5] == 'X' && positions[8] == 'X') TheWinnerIs = 'X';
	        if (positions[3] == 'X' && positions[6] == 'X' && positions[9] == 'X') TheWinnerIs = 'X';
	        if (positions[1] == 'X' && positions[5] == 'X' && positions[9] == 'X') TheWinnerIs = 'X';
	        if (positions[3] == 'X' && positions[5] == 'X' && positions[7] == 'X') TheWinnerIs = 'X';
	        if (TheWinnerIs == 'X' )
	        {System.out.println("<<--The Player with X wins-->>" );
	            return TheWinnerIs;
	        }
	        //Check if O is the winner
	        if (positions[1] == 'O' && positions[2] == 'O' && positions[3] == 'O') TheWinnerIs = 'O';
	        if (positions[4] == 'O' && positions[5] == 'O' && positions[6] == 'O') TheWinnerIs = 'O';
	        if (positions[7] == 'O' && positions[8] == 'O' && positions[9] == 'O') TheWinnerIs = 'O';
	        if (positions[1] == 'O' && positions[4] == 'O' && positions[7] == 'O') TheWinnerIs = 'O';
	        if (positions[2] == 'O' && positions[5] == 'O' && positions[8] == 'O') TheWinnerIs = 'O';
	        if (positions[3] == 'O' && positions[6] == 'O' && positions[9] == 'O') TheWinnerIs = 'O';
	        if (positions[1] == 'O' && positions[5] == 'O' && positions[9] == 'O') TheWinnerIs = 'O';
	        if (positions[3] == 'O' && positions[5] == 'O' && positions[7] == 'O') TheWinnerIs = 'O';
	        if (TheWinnerIs == 'O' )
	        {
	            System.out.println( "<<--The Player with O wins-->>" );
	        return TheWinnerIs; }
	        for(int i=1;i<10;i++)
	        {
	            if(positions[i]=='X' || positions[i]=='O')
	            {
	                if(i==9)
	                {
	                    char Draw='D';
	                    System.out.println(" <<--Draw !-->> ");
	                    return Draw;
	                }
	                continue;
	            }
	            else
	            break;   
	        }
	        return TheWinnerIs;
	    }
	//-------------managing the process of playing -----------------
	 public  void play()
     {
        int spot;
        char blank = ' ';
        do {
            showboard();              
            System.out.println(  "\n\n ----> Player " + getPlayer() +", Please choose a position: " );
            boolean positionTaken = true;
            while (positionTaken) {
                Scanner in = new Scanner (System.in);
                spot=in.nextInt();
                positionTaken = checkPosition(spot);
                if(positionTaken==false)
                positions[spot]=getPlayer();
            }              
            nextPlayer();
        }while ( checkWinner() == blank );
        
    }
	
	
}
