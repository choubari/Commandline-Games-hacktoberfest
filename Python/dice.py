  
# roll the dice
import random
from tinge import colored


def roll():
    return random.randint(1, 6)


if __name__ == "__main__":
    while True:
        val = input(colored("Press Enter to roll the dice or q to quit ", "red"))
        if val.lower() == "q":
            break
        print(colored(f"You have got {roll()}", "blue"))
    print("Thank You for playing")
