import os.path
import random
from enum import Enum
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
    LASER_GUN = 1
    GRAV_BAT = 2
    PLASMA_KNUCKLES = 3
    INSTA_MED = 4
    PIANO_STRING = 5
    MEDIUM_GEARS = 6
    SACK_OF_MYSTERY_MEAT = 7


class Stage(Enum):
    END_8 = 21
    SHATTERED = 20
    END_7 = 19
    END_6 = 18
    END_5 = 17
    POSSIBLE_DOOM = 16
    END_4 = 15
    R3_SECT9_PD = 14
    R3_SECT9 = 13
    SECT5_9 = 12
    END_3 = 11
    END_2 = 10
    SECTOR_5 = 9
    R3 = 8
    R2_L1 = 7
    R2 = 6
    R1_L1 = 5
    L2 = 4
    R1 = 3
    L1 = 2
    START = 1

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
        print(f"Added {item.name.replace('_', ' ').title()} to inventory")
        global adventureText
        adventureText += f"\nAdded {item.name.replace('_', ' ').title()} to inventory"
    def set_health(self, new_health):
        self.health = new_health
    def get_name_pad(self):
        return self.name.__len__() + 2
    def has_weapon(self):
        for item in self.inventory:
            if item.value < 4:
                return True
        return False
    def get_weapons(self):
        weapon_list = []
        for item in self.inventory:
            if item.value < 4:
                weapon_list.append(item)
        return weapon_list



#######################################################################################################################
#
#
# FILE HANDLING FUNCTIONS
#
#
#######################################################################################################################

def load_game(player, saveflag = 0):
    global adventureText
    if save_file_exists & saveflag == 1:
        save = open("adventure.txt", "r")
        adventure_details = save.readlines()
        player_name = adventure_details[0]
        items = adventure_details[1]
        health = adventure_details[2]
        position = adventure_details[3]
        adventureText = adventure_details[4:]
        player.name = player_name
        for item in Item:
            if item.name in items:
                player.add_item(item)
        player.set_health(int(health))
        save.close()
        position = position.strip()
        if position == Stage.START.name:
            start_game(player)
        elif position == Stage.L1.name:
            branch_l1(player, "")
        elif position == Stage.L2.name:
            branch_l2(player, "")
        elif position == Stage.R1.name:
            branch_r1(player, "")
        elif position == Stage.R1_L1.name:
            branch_r1_l1(player, "")
        elif position == Stage.R2.name:
            branch_r2(player, "")
        elif position == Stage.R2_L1.name:
            branch_r2_l1(player, "")
        elif position == Stage.R3.name:
            branch_r3(player, "")
        elif position == Stage.SECTOR_5.name:
            branch_sector_5(player, "")
        elif position == Stage.END_2.name:
            ending2(player, "")
        elif position == Stage.END_3.name:
            ending3(player, "")
        elif position == Stage.SECT5_9.name:
            branch_sect5_9(player, "")
        elif position == Stage.R3_SECT9.name:
            branch_r3_sect9(player, "")
        elif position == Stage.R3_SECT9_PD.name:
            branch_r3_s9_pd(player, "")
        elif position == Stage.END_4.name:
            ending4(player, "")
        elif position == Stage.POSSIBLE_DOOM.name:
            branch_possible_doom(player, "")
        elif position == Stage.END_5.name:
            ending5(player, "")
        elif position == Stage.END_6.name:
            ending6(player, "")
        elif position == Stage.END_7.name:
            ending7(player, "")
        elif position == Stage.SHATTERED.name:
            branch_shattered(player, "")
        elif position == Stage.END_8.name:
            ending8(player, "")
        else:
            print("There was an issue loading game, we will start you at the beginning!\n")
            start_game(player)


    else:
        start_game(player)

def save_game(player, stage, story):
    save_file = open("adventure.txt", "w")
    player_inventory_items = ""
    for item in player.inventory:
        player_inventory_items += item.name + " "
    save_file.write(f"{player.name.strip()}\n{player_inventory_items}\n{player.health}\n{stage.name}\n{story}")
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

    question = f"Choose something to say\n[1]: {speech_choice1[player_name_pad: player_name_pad + 30]}...\nor\n[2]: {speech_choice2[player_name_pad:player_name_pad + 30]}...\nSelection: "
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
    player.name = check_name.title()

    # Declares the narrative string used for this initial starting point
    start_game_string = (f"Kormie: WAKE UP {player.name.upper()} WAKE UP!!! How are you still asleep with all this ruckus?!!?! Nevermind, we haven't much time.\n"
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
    branch_r1_narrative = ("Kormie: What would you like to do first? Would you like to look around your room and find a weapon"
                           "\nor other items that may help you or would you like to try and face the raiders in sector 2 empty-handed?")
    adventureText += branch_r1_narrative
    print(branch_r1_narrative)
    branch_r1_l1_player_txt = f"{player.name}: We should check the room, it would be insane if we walked out there empty handed! "
    branch_r2_player_txt = f"{player.name}: We don't have time for that! We need to get this ship under control!"
    branch_choice = validateInput("1", "2", questionCreator(branch_r1_l1_player_txt, branch_r2_player_txt, player.get_name_pad()))
    if branch_choice == "1":
        branch_r1_l1(player, branch_r1_l1_player_txt)
    else:
        branch_r2(player, branch_r2_player_txt)

def branch_r1_l1(player,branch_text):
    global adventureText
    stage = Stage.R1_L1
    new_branch(player, branch_text, stage)
    narrative = (f"Narrator: You look around the room and find find 3 weapons, (1) a laser gun which can kill pretty much any\n"
                 f"enemy but only has 1 charge, (2)a grav-bat, and (3)a pair of plasma knuckles. You also find an\n"
                 f"(4)insta-med, (5)3 piano strings,(6) 2 medium gears and a (7) 1 sack of mystery meat(?), you can\n"
                 f"only take 2 items (or groups of items)")
    adventureText += narrative
    print(narrative)
    chosenItems = 0
    print("Choose Item #1")
    while chosenItems < 2:
        selection = int(input("Select a number 1 - 7 that correlates to an item to pick that item: "))
        if selection < 1 or selection > 7:
            print("Invalid choice, please try again!")
        else:
            for item in Item:
                if selection == item.value:
                    player.add_item(item)
                    chosenItems += 1
    branch_r2_text = "Let's get a move on, we have a ship to save!\n"
    branch_r2(player, branch_r2_text)




def branch_r2(player,branch_text):
    global adventureText
    stage = Stage.R2
    new_branch(player, branch_text, stage)
    narrative = (f"Narrator: You enter sector 2 and you see bodies strewn about and raiders rummaging through the\n"
                 f"corpses of who used to be your friends and colleagues\n"
                 f"Kormie, whispering: This is so much worse than what I saw only a hour ago..... would you like to\n"
                 f"pick a [fight] these raiders head on or do you want to go through those [vents]?\n"
                 f"I know a special route if we take the vents.\n")
    print(narrative)
    adventureText += narrative
    player_dialogue1 = f"{player.name}: Lets crush these bastards, look at what they have done our people!"
    player_dialogue2 = f"{player.name}: Use the vents, I want to get out of here in one piece!"
    branch_choice = validateInput("1", "2", questionCreator(player_dialogue1, player_dialogue2, player.get_name_pad()))
    if branch_choice == "1":
        branch_r2_l1(player, player_dialogue1)
    else:
        branch_r3(player, player_dialogue2)

def branch_r2_l1(player,branch_text):
    global adventureText
    stage = Stage.R2_L1
    new_branch(player, branch_text, stage)
    has_weapon = player.has_weapon()
    laser = player.checkInventory(Item.LASER_GUN)
    if not has_weapon:
        narrative = ("\nNarrator: You have no weapons so you run at the 2 raiders, you start beating the first raider while Kormie\n"
                     "takes the second one, you are both able to kill the raiders but not without losing some health\n"
                     "-10 health\n")
        player.set_health(90)
        print(narrative)
        adventureText += narrative
    else:
        if laser:
            use_laser = validateInput("y", "n", "Would you like to use your laser charge? (Y or N): ")
            if use_laser == "y":
                narrative = "\nNarrator: You use your laser charge and take down the enemies nearly instantly\n"
                player.inventory.remove(Item.LASER_GUN)
                print(narrative)
                adventureText += narrative
        else:
            narrative= ("\nNarrator: You use your melee weapon to take down one of the enemies, Kormie manages to take\n"
                        "down the other enemy with a little help from you\n")
            print(narrative)
            adventureText += narrative
    player_text = f"{player.name}: That was easy, lets get moving, we've got to get to sector 5"
    branch_sector_5(player,player_text)

def branch_r3(player, branch_text):
    global adventureText
    stage = Stage.R3
    new_branch(player, branch_text, stage)
    narrative = ("Narrator: You and Kormie quietly sneak over to the vent opening and make your way in. Kormie points\n"
                 "out a loose panel on the ceiling of the vent. You reach up and slide it to the side, and climb up,\n"
                 "pulling Kormie behind you. You look around you and notice that this is the security room in\n"
                 "sector 9.\n"
                 "Kormie: This is how I got back here alive, I could have never gotten past the beast the raiders\n"
                 "accidentally let out in sector 5, those numb-skulls\n")
    print(narrative)
    adventureText += narrative
    player_dialogue1 = (f"{player.name}: Well that was the most sightly scene I have ever seen, I am glad we were able to get out of\n"
                        "there alive. Thank you Kormie. I’m glad we don’t have to deal with that normag fendle, I\n"
                        "remember how hard it was to contain when we found it on juineen alpha, Im glad It was on the\n"
                        "smaller side otherwise we would have been toast!")
    player_dialogue2 = f"{player.name}: Yeah yeah yeah, we have a mission we need to get to, no time for chit chat!"
    player_dialogue_choice = validateInput("1", "2", questionCreator(player_dialogue1,player_dialogue2,player.get_name_pad()))
    if player_dialogue_choice == "1":
        print(player_dialogue1)
        adventureText += player_dialogue1
    elif player_dialogue_choice == "2":
        print(player_dialogue2)
        adventureText += player_dialogue2
    narrative2 = (f"Narrator: The room has been picked clean so there is no point in looking around, you and Kormie head\n"
                  f"for the door, but you notice the door won’t open.\n"
                  f"Kormie: Ah shit, I must’ve kicked the lockdown box when I was trying to get the door closed,\n"
                  f"everything went so fast, I.. I was getting chased, Im so sorry {player.name}."
                  f"\n{player.name}: Let me see what I can do.\n")
    print(narrative2)
    adventureText += narrative2
    if player.checkInventory(Item.MEDIUM_GEARS):
        branch_text = (f"{player.name}: It looks like I have just what we need right here! Let me just put this in here\n"
                       f"Uhhhhh, yeah I think that goes, there, then we do that, *click* *tuk tuk tuk tuk tuk*\n"
                       f"Narrator: The door opens up with ease!\n"
                       f"Kormie: How did you do that? That takes some serious skill! Be very quiet going out that door,\n"
                       f" the raider that chased me is right outside.\n")
        branch_r3_sect9(player, branch_text)
    elif not player.has_weapon():
        branch_text = ("Narrator: You head back down into the vents, you dont get to sector 9 like before but the vent\n"
                       "lands you right at the entrance of sector 3. You did not have to deal with the raiders in sector 3\n")
        branch_sector_5(player, branch_text)
    else:
        player_dialogue3 = (f"{player.name}: Lets go back, I dont know whats on the other side of that glass, I don't\n"
                            f"want to draw more attention than needed to ourselves\n"
                            f"Narrator: You head back down into the vents, you dont get to sector 9 like before but the vent\n"
                            f"lands you right at the entrance of sector 3. You did not have to deal with the raiders in sector 3\n")
        player_dialogue4 = f"{player.name: *breaks the glass* That should do it!}"
        branch_choice = validateInput("1", "2", questionCreator(player_dialogue3,player_dialogue4, player.get_name_pad()))
        if branch_choice == "1":
            branch_sector_5(player, player_dialogue3)
        else:
            branch_shattered(player, player_dialogue4)


def branch_sector_5(player,branch_text):
    global adventureText
    stage = Stage.SECTOR_5
    new_branch(player, branch_text, stage)
    narrative = ("Narrator: You head through sector 3 and 4, the rooms riddled with bodies, a horrific scene, but you\n"
                 "pass through with no interruption by any raiders, only their path of destruction. You arrive at the\n"
                 "door to sector 5. You press the open sector button, the red spinning lights turn on, the alarms\n"
                 "blaring. As the doors open you realize you have made a grave mistake, you and kormie are face to\n"
                 "face with a normag fendle, a giant 20 foot snarling beast with scales and feathers, similar to what\n"
                 "we believe dinosaurs to have looked like but with a far more aggressive and intimidating build,\n"
                 "bearing rows upon rows of sharp, jagged teeth and a surprisingly but sickeningly sweet hot breath.\n")
    print(narrative)
    adventureText += narrative
    has_meat = player.checkInventory(Item.SACK_OF_MYSTERY_MEAT)
    has_laser = player.checkInventory(Item.LASER_GUN)
    if has_meat:
        ending2txt = ("Narrator: you pull out the sack of mystery meat and the normag, surprisingly, sits down and begs\n"
                      "like a dog for the sack of meat, it appears that you have tamed the normag, the most formidable\n"
                      "beast in this star system!\n")
        ending2(player, ending2txt)
    elif has_laser:
        narrative2 = ("Narrator: The normag swats at you and Kormie, both of you fall to the ground with some very deep cuts the\n"
                      "beast starts leaning down to you to, you believe, take a bite out of you. The normag starts roaring\n"
                      "you quickly pull out your laser and take a shot into the beasts mouth while it is roaring at you.\n"
                      "The beast falls instantly, you have taken out the beast, once thought to be unkillable, you found\n"
                      "its weakspot.\n"
                      "-80 health\n"
                      "Kormie: You are literally insane, there is no way you pulled that off, the whole crew of lormat 15\n"
                      "couldn't even take that thing down, you’ve got some great aim. Do you have any insta-med that we\n"
                      "could use? We barely have any health left.\n")
        player.inventory.remove(Item.LASER_GUN)
        print(narrative2)
        adventureText += narrative2
        has_med = player.checkInventory(Item.INSTA_MED)
        if has_med:
            player_narrative = (f"{player.name}Luckily, I do, let's both take an injection and get out of here.\n"
                                "+50 health\n")

        else:
            player_narrative = f"{player}: We are just going to have to tough it through. You move towards sector 9 doors.\n"
        branch_sect5_9(player, player_narrative)

    else:
        narrative2 = ("Narrator: You attempt to swing at the normag but your attempts are futile, the normag lets out a\n"
                      "snort, either as a slight chuckle or annoyed grunt. The normag turns to you and bites both of\n"
                      " your arms off and slurps you up, almost all in one motion. \nYou are dead\n")
        ending3(player, narrative2)


def ending2(player, branch_text):
    global adventureText, play
    stage = Stage.END_2
    new_branch(player, branch_text, stage)
    narrative = ("Narrator: You and Kormie jump on the normags back and ride him into the polyhedron deck. When you break down\n"
                 "the doors, all of the raiders cower in fear and disbelief. Nobody has ever seen a tamed normag. You\n"
                 "get off the back of the normag and free the flight crew that had been held hostage by the raiders.\n"
                 "You tie up the raiders and they are put in the holding deck in different cells. The ship has had\n"
                 "many casualties, but you saved the homeship.\n")
    print(narrative)
    adventureText += narrative
    save_game(player, stage, adventureText)
    play = False


def ending3(player, branch_text):
    global adventureText, play
    stage = Stage.END_3
    new_branch(player, branch_text, stage)
    play = False


def branch_sect5_9(player, branch_text):
    global adventureText
    stage = Stage.SECT5_9
    new_branch(player, branch_text, stage)
    narrative = ("Narrator: You and Kormie open the polyhedron deck doors and are met with 5 raiders staring you down,\n"
                 " you see whats left of the flight crew tied up and gagged. The raiders brandish their weapons.")
    print(narrative)
    adventureText += narrative
    if player.has_weapon():
        if player.health > 50:
            narrative2 = ("Narrator: You manage to beat down the raiders, it is a battle fought hard. You are holding on by a thread\n"
                          "though. You have saved the ship but spend 2 in rehabilitation, and are still not back where\n"
                          "you were before the fight. Those raiders were ruthless but you were stronger...")
        else:
            narrative2 = ("Narrator: You manage to kill the raiders, but with your final blow, you collapse as well. The\n"
                          "battle was fierce yet quick, but sadly you did not survive. Kormie grieved for many years over\n"
                          "your death but you would have been happy that you saved the ship...")
    else:
        narrative2 = ("Narrator: You ran into the room with a heart full of confidence and empty hands. The raiders nearly\n"
                      "instantly kill you and Kormie, they laugh at you for trying to go up against them without any\n"
                      "weapons. Honestly, I am laughing too, that's pretty ridiculous, the ship is in raider hands and\n"
                      "ends up being used for many atrocities...")
    ending7(player, narrative2)


def branch_r3_sect9(player, branch_text):
    global adventureText
    stage = Stage.R3_SECT9
    new_branch(player, branch_text, stage)
    player_dialogue1 = f"{player.name}: Noted, lets sneak behind those crates and see if we can sneak to the door to the polyhedron deck"
    player_dialogue2 = f"{player.name}: Lets kill that bastard, its what he deserves, he hasn’t seen us yet so it should be pretty easy."
    branch_decision = validateInput("1", "2", questionCreator(player_dialogue1, player_dialogue2, player.get_name_pad()))
    if branch_decision == "1":
        chance = random.randint(1,10)
        if chance < 3:
            narrative = "Narrator: You sneak past the raider and move towards the polyhedron deck doors.\n"
        else:
            narrative = ("Narrator: The raider sees you and starts charging towards you, see him and quickly move out of\n"
                         "the way, he slams into the wall and dies instantly.\n"
                         "Kormie: There’s no way.... *chuckles*\n"
                         "Narrator: You move towards the polyhedron deck doors.\n")
    else:
        narrative = ("Narrator: You sneak up behind the raider and strangle him, and he dies quickly.\n"
                     "Kormie: You are one insane son of a bitch, let’s get to the polyhedron deck and get this ship\n"
                     "back in control!\n")

    branch_r3_s9_pd(player, narrative)

def branch_r3_s9_pd(player, branch_text):
    global adventureText
    stage = Stage.R3_SECT9_PD
    new_branch(player, branch_text, stage)
    narrative = ("Narrator: You sneak into the polyhedron deck, you see a group of 5 raiders and the flight crew who\n"
                 "they tied up but they do not see you.\n")
    print(narrative)
    adventureText += narrative
    player_dialogue1 = f"{player.name}: Lets untie the flight crew and have them help us fight the raiders"
    player_dialogue2 = f"{player.name}: Lets go over to the control console I have an idea..."
    branch_choice = validateInput("1", "2", questionCreator(player_dialogue1, player_dialogue2, player.get_name_pad()))
    if branch_choice == "1":
        ending4(player, player_dialogue1)
    else:
        branch_possible_doom(player, player_dialogue2)


def ending4(player, branch_text):
    global adventureText, play
    stage = Stage.END_4
    new_branch(player, branch_text, stage)
    narrative = ("Narrator: You and Kormie are able to untie the crew and are all able to get the jump on the\n"
                   "raiders, all the raiders go down with ease, the day is saved, but there are many casualties.\n")
    print(narrative)
    adventureText += adventureText
    save_game(player, stage, adventureText)
    play = False

def branch_possible_doom(player, branch_text):
    global adventureText
    stage = Stage.POSSIBLE_DOOM
    new_branch(player, branch_text, stage)
    narrative = ("Narrator: With your previous experience in the space force, you are able to aim all the ships planet\n"
                 "ender cannons at the raiders home planet\n")
    print(narrative)
    adventureText += narrative
    player_dialogue1 = (f"{player.name}: *yells* Hey shitheads, Ive got every cannon on this thing aimed for your home world, call off\n"
                        "all of your people or I will eradicate your entire planet")
    player_dialogue2 = (f"{player.name}: Im going to kill the rest of their kind........ *click*\n"
                        "Narrator: You press the button, you feel nothing, you've doomed billions to a nearly instant\n"
                        " death, you've had too many run-ins with these people to have empathy for them anymore.")
    branch_choice = validateInput("1", "2", questionCreator(player_dialogue1, player_dialogue2, player.get_name_pad()))
    if branch_choice == "1":
        ending5(player, player_dialogue1)
    else:
        ending6(player, player_dialogue2)



def ending5(player, branch_text):
    global adventureText, play
    stage = Stage.END_5
    new_branch(player, branch_text, stage)
    narrative = (f"Raider Leader: You would not do that, you would never.\n"
                 f"{player.name}: I absolutely would, don’t force my hand.\n"
                 f"Narrator: The raiders stand down and you are able to take them into custody. You untie the crew and\n"
                 f"are able to put the raiders into the holding deck into individual cells, you have saved the home ship.\n")
    print(narrative)
    adventureText += narrative
    save_game(player, stage, adventureText)
    play = False

def ending6(player, branch_text):
    global adventureText
    stage = Stage.END_6
    new_branch(player, branch_text, stage)
    narrative = (f"{player.name} screams to the raiders: Ive just blown up your home planet, you all deserve it, i've\n"
                 f"seen the atrocities you have committed. You can kill me but you have nothing you are fighting for\n"
                 f"anymore, there is nobody back home waiting for you, they are all gone. Every. Last. One.\n"
                 f"Narrator: The raiders are filled with immense anger and sadness, the leader shoots you, killing you\n"
                 f"and shoots Kormie killing him as well. The other raiders kill the rest of the crew. You would have\n"
                 f"believed this to have been a win, but all it was was a blood bath.... \n")
    print(narrative)
    adventureText += narrative
    save_game(player, stage, adventureText)

def ending7(player, branch_text):
    global adventureText, play
    stage = Stage.END_7
    new_branch(player, branch_text, stage)
    play = False

def branch_shattered(player, branch_text):
    global adventureText
    stage = Stage.SHATTERED
    new_branch(player, branch_text, stage)
    narrative = ("Narrator: You smash the window open with your weapon, a raider comes over and confronts you\n"
                "Kormie screams: What the hell are you doing?!?! That’s the one that chased me in here!"
                "Narrator: The raider pushes you to the ground, your weapon flies to the other side of the window and\n"
                "the raider goes for Kormie, he starts beating Kormie senseless screaming and laughing while in the\n"
                "act\n"
                "Raider: I’ve got you now you slimey bastard! You will all pay for what you did to our people!!!\n")
    print(narrative)
    adventureText += narrative
    if player.checkInventory(Item.PIANO_STRING):
        narrative = ("Narrator: You quickly pull out the piano wire and strangle the raider, you do it quick enough to\n"
                     "to save Kormie.\n"
                     "Kormie: I owe my life to you, {name}, thank you so much.\n"
                     "Narrator: You head towards the doors to the polyhedron deck.\n")
        branch_sect5_9(player, narrative)
    else:
        narrative = ("Narrator: You kill the raider, but Kormie is bleeding out on the floor. Unfortunately, you do not\n"
                     "have an insta-med and Kormie, and your best friend of 20 years dies in your arms. You jump back\n"
                     "out of the window with a flame in your heart, a flame of vengeance. You pick back up your weapon\n"
                     "and run towards the polyhedron deck doors.\n")
        ending8(player, narrative)

def ending8(player, branch_text):
    global adventureText, play
    stage = Stage.END_8
    new_branch(player, branch_text, stage)
    narrative = ("Narrator: You run into the polyhedron deck and you start tearing apart the raiders, you fail to count\n"
                 "how many but that doesn’t matter, the only thing you want is vengeance. The adrenaline allows you to\n"
                 "kill all the remaining raiders.\n"
                 "Narrator: You manage to free all of the flight crew, but they will never be able to look at you the\n"
                 "same after seeing what you did to those raiders. But the only thing that matters is that you saved\n"
                 "the ship.... its what Kormie would have wanted.")
    print(narrative)
    adventureText += narrative
    save_game(player,stage, adventureText)
    play = False

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


