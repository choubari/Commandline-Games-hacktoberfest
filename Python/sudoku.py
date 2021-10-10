from colorama import Fore, Back, Style

game_running = False

'''
Sudoku game in terminal, made by TimeSauce
'''

# Create board
def create_board(bo):
    print(Fore.CYAN)
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print(Fore.GREEN + "- - - - - - - - - - - - - " + Fore.CYAN)

        for j in range(9):
            if j % 3 == 0 and j != 0:

                print(Fore.GREEN + " | " + Fore.CYAN, end="")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")
    print(Fore.WHITE)

# Main game function
def game():
    global board
    game_running = True
    chosen_numb = 0

    # Game board
    board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0 ],
            [6, 0, 0, 1, 9, 5, 0, 0, 0 ],
            [0, 9, 8, 0, 0, 0, 0, 6, 0 ],
            [8, 0, 0, 0, 6, 0, 0, 0, 3 ],
            [4, 0, 0, 8, 0, 3, 0, 0, 1 ],
            [7, 0, 0, 0, 2, 0, 0, 0, 6 ],
            [0, 6, 0, 0, 0, 0, 2, 8, 0 ],
            [0, 0, 0, 4, 1, 9, 0, 0, 5 ],
            [0, 0, 0, 0, 8, 0, 0, 7, 9 ]
    ]

    create_board(board)
    while game_running:
        print("Whenever you wish to end the game, type 'end' ")
        
        # Check if first 2 user inputs are valid
        try:
            chosen_row = input("Choose a row, from 1-9: \n")
            if chosen_row == 'end':
                game_running = False
                break
            chosen_row = int(chosen_row) - 1

            chosen_spot = input("Choose a spot, from 1-9: \n")
            if chosen_spot == 'end':
                game_running = False
                break
            chosen_spot = int(chosen_spot) - 1
            
            # Check if user number can be added to the board
            if board[chosen_row][chosen_spot] == 0:
                chosen_numb = input("What number to add, from 1-9: \n")
                if chosen_numb == 'end':
                    game_running = False
                    break
                board[chosen_row][chosen_spot] = Fore.RED + chosen_numb + Fore.CYAN
                create_board(board)
                print(Fore.WHITE)

            else:
                print("This spot is taken!")
                continue

        except ValueError:
            print("Wrong input!")
            continue

    # Check if the player won
    if not game_running:
        rows = check_rows() + 1
        columns = check_columns() + 1 

        if rows == len(board) and columns == len(board):
            print("You have won!")
            game2()
        else:
            print("You have lost!")
            game2() 

# Check rows
def check_rows():
    correct_x = 0
    for x in range(len(board)):
        for y in board[x]:
            if y == 0:
                break
                continue
        if len(board[x]) == len(set(board[x])):
            correct_x += 1
    return correct_x

# Check columns 
def check_columns():
    correct_y = 0
    column_count = 0
    numbers = []
    checking_y = True
    x = 0

    while checking_y:
        if board[x][column_count] == 0:
            continue
        numbers.append(board[x][column_count])
        x += 1
        if x == 9:
            x = 0
            column_count += 1
            if len(numbers) == len(set(numbers)):
                correct_y += 1

            numbers = []
            if column_count == len(board):
                checking_y = False
    return correct_y

# New game
def game2():
    user = str(input("Would you like to play again?" + Fore.GREEN + "y" + Fore.WHITE + "/" + Fore.RED + "n" + Fore.WHITE +"\n"))

    if user == 'y':
        game()
    elif user == 'n':
        print("Aight, see you next time!")
    else:
        print("Enter the right letter!")
        game2()

game()
