import random


def main():
    computer = random.choice(["rock", "paper", "scissor"])
    user = input("Guess any one from -> rock paper scissor: ")
    print("opponent choice : {}".format(computer))

    if computer == user:
        print("Tie")
    elif computer == "paper" and user == "scissor":
        print("{0} cuts {1}\ncongrats You win!".format(user, computer), "\U0001F929")
    elif computer == "paper" and user == "rock":
        print("{1} covers {0}\noops You lost!".format(user, computer), "\U0001F972")
    elif computer == "scissor" and user == "paper":
        print("{1} cuts {0}\noops You lost!".format(user, computer), "\U0001F972")
    elif computer == "scissor" and user == "rock":
        print("{0} smashes {1}\ncongrats You win!".format(user, computer), "\U0001F929")
    elif computer == "rock" and user == "scissor":
        print("{1} smashes {0}\noops You lost!".format(user, computer), "\U0001F972")
    elif computer == "rock" and user == "paper":
        print("{0} covers {1}\ncongrats You win!".format(user, computer), "\U0001F929")
    playagain()


def playagain():
    """Ask user if he/she wants to play again or not"""

    if input("Would you like to play again (Yes/No)? ").lower().startswith("y"):
        main()
    else:
        print("Leaving so soon, we will miss you", "\U0001F97A")


if __name__ == "__main__":
    main()
