import os.path
import string
from enum import Enum
from symtable import Class
import re
save_file_exists = os.path.isfile("adventure.txt")

name = os.getlogin()

play = True
adventureText = ""






class Item(Enum):
    SACK_OF_MEAT = 1
    MEDIUM_GEARS = 2
    PIANO_STRING = 3
    PLASMA_KNUCKLES = 4



class Player:
    def __init__(self):
        self.name = ""
        self.health = 100
        self.inventory = []

    def checkInventory(self, item):
        flag = any(x == item for x in self.inventory)
        return flag
    def add_item(self, item):
        self.inventory.append(item)
    def set_health(self, new_health):
        self.health = new_health


def load_game(player, story_text):
    if save_file_exists:
        save = open("adventure.txt", "r")
        adventure_details = save.readlines()
        player_name = adventure_details[0]
        items = adventure_details[1]
        health = adventure_details[2]
        position = adventure_details[3]
        player.set_name(player_name)
        for item in Item:
            if item.name in items:
                player.add_item(item)
        player.set_health(int(health))
        save.close()
        # need to put if elif else branch here to put the player back into the place they were before exiting
    else:
        start_game(player, story_text)
def save_game(player, stage, story):
    save_file = open("adventure.txt", "w")
    save_file.write(player.name + "\n" + player.inventory + "\n" + player.health + "\n" + stage + "\n" + story)
    save_file.close()

def validateInput(choice1, choice2, question):
    valid = False
    choice1 = choice1.lower()
    choice2 = choice2.lower()
    while not valid:
        userChoice = input(question).lower()
        if userChoice == choice1:
            return choice1
        elif userChoice == choice2:
            return choice2
        else:
            print("Invalid input, please try again")
    return None
# beginning function
def start_game(player, story_text):
    if player.__name__ == "":
        check_name = input("Enter your name: ")
        while True:
            if len(check_name.strip()) == 0:
                print("Name cannot be empty")
            elif not re.match(r"^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$", check_name):
                print("Invalid name format")
            else:
                print("Valid name")
                break
        player.__name__ = check_name

    start_game_string = (f"WAKE UP {player.__name__} WAKE UP!!! How are you still asleep with all this ruckus?!!?! Nevermind, we havent much time.\n"
          "Our ship has sustained significant damage, raiders have invaded sectors 2, 5, 9, and have even infiltrated\n"
          "the polyhedron deck and have taken Captain Montak and the whole flight crew hostage! I hate to say it but\n"
          "you and I may be the only ones that have not been captured or executed\n")
    story_text += start_game_string
    print(start_game_string)






while play:
    mainPlayer = Player
    choice = validateInput("y", "n", "You seem to have stumbled into cartridge that contains lost memories of yours\n"
          "would you like to see what has been kept from you for so long (Y or N): ")
    if choice == "n":
        print("Well, that was a waste of time, goodbye")
        break
    elif choice == "y":
        print("Well then, lets get started")


        load_game(mainPlayer)



