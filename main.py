import os.path
import string
from enum import Enum
from symtable import Class
import re

#######################################################################################################################
#
#
# GLOBAL VARIABLES
#
#
#######################################################################################################################

# Checks to see if there is an existing game save
save_file_exists = os.path.isfile("adventure.txt")

# Holds the variable that will determine if the game will continue
play = True

# Holds the whole game story
adventureText = ""

#######################################################################################################################
#
#
# CLASS DECLARATIONS
#
#
#######################################################################################################################

class Item(Enum):
    SACK_OF_MEAT = 1
    MEDIUM_GEARS = 2
    PIANO_STRING = 3
    PLASMA_KNUCKLES = 4

class Stage(Enum):
    R2 = 6
    R1_L1 = 5
    L2 = 4
    START = 1
    L1 = 2
    R1 = 3

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
    def get_name_pad(self):
        return self.name.__len__() + 2


#######################################################################################################################
#
#
# FILE HANDLING FUNCTIONS
#
#
#######################################################################################################################

def load_game(player, flag = 0):
    if save_file_exists & flag == 1:
        save = open("adventure.txt", "r")
        adventure_details = save.readlines()
        player_name = adventure_details[0]
        items = adventure_details[1]
        health = adventure_details[2]
        position = adventure_details[3]
        player.name = player_name
        for item in Item:
            if item.name in items:
                player.add_item(item)
        player.set_health(int(health))
        save.close()
        # need to put if elif else branch here to put the player back into the place they were before exiting
    else:
        start_game(player)

def save_game(player, stage, story):
    save_file = open("adventure.txt", "w")
    player_inventory_items = ""
    for item in player.inventory:
        player_inventory_items += item.name + " "
    save_file.write(f"{player.name}\n{player_inventory_items}\n{player.health}\n{stage.name}\n{story}")
    save_file.close()

#######################################################################################################################
#
#
# ESSENTIAL GAME FUNCTIONS
#
#
#######################################################################################################################

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
def questionCreator(speech_choice1, speech_choice2, player_name_pad = 0):

    question = f"Choose something to say\n[1]: {speech_choice1[player_name_pad: player_name_pad + 20]}...\nor\n[2]: {speech_choice2[player_name_pad:player_name_pad + 20]}...\nSelection: "
    return question

def new_branch(player,branch_text, stage):
    global adventureText
    adventureText += "\n" + branch_text
    print(branch_text)
    save_game(player, stage, adventureText)

#######################################################################################################################
#
#
# START OF GAME BRANCHES
#
#
#######################################################################################################################

# Function to start game
def start_game(player):
    global adventureText
    # Getting the player name
    check_name = input("Enter your name: ")
    while True:
        if len(check_name.strip()) == 0:
            print("Name cannot be empty")
        elif not re.match(r"^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$", check_name):
            print("Invalid name format")
        else:
            print("Valid name")
            break
    player.name = check_name

    # Declares the narrative string that is used for this initial starting point
    start_game_string = (f"Kormie: WAKE UP {player.name} WAKE UP!!! How are you still asleep with all this ruckus?!!?! Nevermind, we havent much time.\n"
          "Our ship has sustained significant damage, raiders have invaded sectors 2, 5, 9, and have even infiltrated\n"
          "the polyhedron deck and have taken Captain Montak and the whole flight crew hostage! I hate to say it but\n"
          "you and I may be the only ones that have not been captured or executed")
    # Adds the narrative text to the adventure string
    adventureText += start_game_string
    print(start_game_string)
    branch_l1_text = f"{player.name}: Ughhhhhhh, I'm so tireeedddd, let me sleep for just like 15 more minutes"
    branch_r1_text = (f"{player.name}: God, that's horrible, I don't know how I slept so deeply! We must gain back control"
                 f"\nof the ship before their ‘pilots’ fly us straight into a black hole... or worse...  Let’s get a move"
                 f"\non, we cant have much time!")
    top_branch_choice = validateInput("1", "2", questionCreator(branch_l1_text, branch_r1_text, player.get_name_pad()))
    if top_branch_choice == "1":
        branch_l1(player, branch_l1_text)
    elif top_branch_choice == "2":
        branch_r1(player, branch_r1_text)


def branch_l1(player,branch_text):
    stage = Stage.L1
    new_branch(player, branch_text, stage)
    branch_l2_text = (f"{player.name}: zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz.........zzzzzzzzzzzzzzzzzzz................\n"
                      f"zzzzzzzzzzzzzzzzz............zzzzzzzzzzzzzzzzzzzzzzzzzzzz...............")
    branch_l1_r1_text = f"{player.name}: You’re right! Let’s crush these scum and take back control of our home-ship!"
    branch_choice = validateInput("1", "2", questionCreator(branch_l2_text, branch_l1_r1_text, player.get_name_pad()))
    if branch_choice == "1":
        branch_l2(player, branch_l2_text)
    elif branch_choice == "2":
        branch_r1(player, branch_l1_r1_text)

def branch_l2(player,branch_text):
    global adventureText
    global play
    stage = Stage.L2
    new_branch(player, branch_text, stage)
    ending1 = ("\nKormie tried to take care of the situation by himself and didn’t get very far. The raiders in the control\n"
          "room got wind of some crew that were trying to resist against them, they tried detaching your portion of the\n"
          "ship and failed horribly killing all on board, including themselves")
    adventureText += ending1
    print(ending1)
    save_game(player,stage, adventureText)

    play = False


def branch_r1(player,branch_text):
    global adventureText
    stage = Stage.R1
    new_branch(player, branch_text, stage)
    branch_r1_narrative = ("What would you like to do first? Would you like to look around your room and find a weapon"
                           "\nor other items that may help you or would you like to try and face the raiders in sector 2 empty-handed?")
    adventureText += branch_r1_narrative
    print(branch_r1_narrative)
    branch_r1_l1_player_txt = f"{player.name}: We should check the room, it would be insane if we walked out there empty handed! "
    branch_r2_player_txt = f"{player.name}: We don't have time for that! We need to get this ship under control!"
    branch_r1_choice = validateInput("1", "2", questionCreator(branch_r1_l1_player_txt, branch_r2_player_txt, player.get_name_pad()))

def branch_r1_l1(player,branch_text):
    global adventureText
    stage = Stage.R1_L1
    new_branch(player, branch_text, stage)


def branch_r2(player,branch_text):
    global adventureText
    stage = Stage.R2
    new_branch(player, branch_text, stage)
#
# def branch_r1(player,branch_text):
#     global adventureText
#     stage = Stage.R1
#     new_branch(player, branch_text, stage)
#
# def branch_r1(player,branch_text):
#     global adventureText
#     stage = Stage.R1
#     new_branch(player, branch_text, stage)
#
# def branch_r1(player,branch_text):
#     global adventureText
#     stage = Stage.R1
#     new_branch(player, branch_text, stage)
#
#
# def branch_r1(player, branch_text):
#     global adventureText
#     stage = Stage.R1
#     new_branch(player, branch_text, stage)
#
#
# def branch_r1(player, branch_text):
#     global adventureText
#     stage = Stage.R1
#     new_branch(player, branch_text, stage)
#
#
# def branch_r1(player, branch_text):
#     global adventureText
#     stage = Stage.R1
#     new_branch(player, branch_text, stage)
#
#
# def branch_r1(player, branch_text):
#     global adventureText
#     stage = Stage.R1
#     new_branch(player, branch_text, stage)
#
#
# def branch_r1(player, branch_text):
#     global adventureText
#     stage = Stage.R1
#     new_branch(player, branch_text, stage)


#######################################################################################################################
#
#
# BEGINNING OF GAME
#
#
#######################################################################################################################
while play:
    mainPlayer = Player()
    choice = validateInput("y", "n", "You seem to have stumbled into cartridge that contains lost memories of yours\n"
          "would you like to see what has been kept from you for so long (Y or N): ")
    if choice == "n":
        print("Well, that was a waste of time, goodbye")
        break
    elif choice == "y":
        print("Well then, lets get started")
        flag = 0
        if save_file_exists:
            save_game_continue = validateInput("y", "n", "We see that you have a saved game in"
                                                         "\nprogress, would you like to continue?(Y or N): ")
            if save_game_continue == "n":
                with open("adventure.txt", "w") as file:
                    pass
                flag = 0
            else:
                flag = 1
        load_game(mainPlayer, flag)


