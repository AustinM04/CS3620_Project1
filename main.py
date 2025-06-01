import os
name = os.getlogin()
play = True

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


while play:
    choice = validateInput("y", "n", "You seem to have stumbled into cartridge that contains lost memories of yours\n"
          "would you like to see what has been kept from you for so long (Y or N): ")
    if choice == "n":
        print("Well, that was a waste of time, goodbye")
        break
    elif choice == "y":
        print("Well then, lets get started")



