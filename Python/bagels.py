"""
Auther: Mahmoud Fettal
Github: MahmoudFettal

Welcome to bagels a simple but fun terminal game
Goal:
    Guess a randomly generated number of 3 digits (no digit will be repeated) in under 10 guess.
Rules:
    the user must guess a number and he will have 3 clues, abd they are as follows:
        Pico it means that one digit is correct but in the wrong position.
        Fermi it means that One digit is correct and in the right position.
        Bagels it means that No digit is correct.
"""

import random

WELCOME = """ Welcome to bagels, I will think of a random 3 digits number
(no digit will be repeated) and you have to guess it.
When I say:
    Pico it means that one digit is correct but in the wrong position.     
    Fermi it means that One digit is correct and in the right position.     
    Bagels it means that No digit is correct. 
"""

PLAY_AGAIN = "Do you want to play again? (yes or no): "

def get_random_number():
    """
    This function generates the secret number!

    Returns:
        str: secret number
    """
    secret_numbers = []

    for _ in range(3):
        digit = random.randint(1,9)
        while str(digit) in secret_numbers:
            digit = random.randint(1,9)

        secret_numbers.append(str(digit))

    return ''.join(secret_numbers)

def bagels():
    """
    This function contians the logic of one round of the game.
    """
    secret = get_random_number()
    print("\nI have thought up a number. You have 10 guesses to get it.")

    for attempt in range(1,11):
        guess = input(f"Guess #{attempt}: ")
        while len(guess) != 3:
            guess = input(f"Guess #{attempt} (please give a valid 3 digits number): ")
        simlarity = 0

        if guess == secret:
            print("You got it, Great Job!")
            return

        for i in range(3):
            if guess[i] == secret[i]:
                print("Fermi", end=" ")
                simlarity += 1
            elif guess[i] in secret:
                print("Pico", end=" ")
                simlarity += 1

        if simlarity == 0:
            print("Bagels")
        else:
            print()

    print(f"You have no more guess, the answer is {secret}.\nGood luck next time!")

if __name__ == '__main__':
    print(WELCOME, end="")

    PLAY = True

    while PLAY:
        bagels()
        PLAY = input(PLAY_AGAIN) in ["Yes", "yes"]

    print("\nGood bye!")
