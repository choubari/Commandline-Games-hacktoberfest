import random
import time


def display_intro():
    print("You are in a land full of drangons. In front of you,")
    print("you see two caves. In one cave, the dragon is friendly")
    print("and will share his treasure with you. The other dragon")
    print("is greedy and hungry, and will eat you on sight.")


def choose_cave() -> int:
    cave = ""
    while cave != "1" and cave != "2":
        print("Which cave will you go into? (1 or 2)", end=" ")
        cave = input()

    return int(cave)


def check_cave(choose_cave: int):
    print("You approach the cave...")
    time.sleep(2)
    print("It is dark and spooky...")
    time.sleep(2)
    print("A large dragon jumps out in front of you!")
    print("He opens his jaws in from of you and...")
    print()
    time.sleep(2)

    friendly_cave = random.randint(1, 2)

    if choose_cave == friendly_cave:
        print("Gives you his treasure!")
    else:
        print("Gobbles you down in one bite!")


def playagain() -> bool:
    """ask user to play again"""
    return input("Would you like to play again (Yes/No)? ").lower().startswith("y")


def main():
    while True:
        display_intro()
        cave_number = choose_cave()
        check_cave(cave_number)

        if not playagain():
            return


if __name__ == "__main__":
    main()
