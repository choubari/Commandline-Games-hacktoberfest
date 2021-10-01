import random

from tinge import colored


def welcome():
    """Welcome new user and explain rules of the game"""
    print(colored("Hello there \U0001F60A, Welcome to Guess the Number game", "green"))
    print("Game Rule -> ")
    print(
        "In this game you have to guess a number and you will have total 5 chances to guess it correct"
        "\n"
        "You guess should be in between 1 and 25"
    )


def user_input():
    """Ask user to guess a number, if input is valid digit then return the user_input"""
    user_number = input("Guess a number: ")
    try:
        user_number = int(user_number)
    except:
        print("Please ender a valid digit!")
        return user_input()
    else:
        if 1 <= user_number <= 25:
            return user_number
        else:
            print("You need to enter a digit between 0 and 50")
            return user_input()


def success(count: int):
    """Print the sucess message when user guess the correct number"""
    positions = ["1st", "2nd", "3rd", "4th", "5th"]
    print(
        colored(
            f"Wow!\U0001F929, you have won the game in {positions[count-1]} try",
            "green",
        )
    )


def playagain():
    """Ask user if he/she wants to play again or not"""
    if input("Would you like to play again (Yes/No)? ").lower().startswith("y"):
        main()
    else:
        print("Leaving soon, we will miss you", "\U0001F97A")
        print(colored("Thanks for playing, Made with \u2665 by g-paras", "blue"))


def main():
    welcome()
    number = random.randint(1, 25)
    # number = 18    # used while testing
    count = 0
    MAX_COUNT = 5
    while count < MAX_COUNT:
        user_number = user_input()

        count += 1
        if user_number == number:
            success(count)
            playagain()
            break
        elif user_number < number:
            print(colored("Number is too small", "red"))
        else:
            print(colored("Number is too big", "red"))

        if count == MAX_COUNT:
            print("You have exhausted all the chances, better luck next time.")
            playagain()


if __name__ == "__main__":
    main()
