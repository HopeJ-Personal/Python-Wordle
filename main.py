## Instal
import os
os.system('pip install termcolor')
os.system('pip install --upgrade pip')

## Import
import random
import configparser
import termcolor
from termcolor import colored

## Setup Basic Functions
def clear_screen():
    # Check if the operating system is Windows ('nt')
    if os.name == 'nt':
        _ = os.system('cls')  # Use 'cls' for Windows
    else:
        _ = os.system('clear') # Use 'clear' for Linux/macOS

## File Path
wordlist = "wordlist.txt"
config = "config.ini"

## Config
config = configparser.ConfigParser()
config.read('config.ini')

## Variables: Config
debug_print = config['debug']['debug_print']
debug_noclear = config['debug']['debug_noclear']
file_path = config['path']['wordlist']
rounds = int(config['wordle']['rounds'])
#print(debug_print)

## Qol functions
def dprint(string):
    if debug_print == 'true':
        print(string)

def get_word():
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    
        # Optional: Remove newline characters from each line
        lines = [line.strip() for line in lines]
        random_line = random.choice(lines)
        
        return random_line

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

## Variables: Game
goal_word = get_word()

dprint(config['debug']['debug_print'])
dprint("test debug print")

#py sectioned-main.py

# Step 1
# Letters in both words
def evaluate(input_word):
    # Variables: Temporary
    flag_list = [0, 0, 0, 0, 0]

    ## Create check list(s)
    check_yellow_list = []
    check_red_list = []

    ## Variables: Regular
    global goal_word
    goal_word_unp = [ *goal_word ]
    input_word_unp = [ *input_word ]

    ## Variables: Distinct
    goal_word_unp_unique = list(set(goal_word_unp))
    input_word_unp_unique = list(set(input_word_unp))
    dprint(goal_word)

    ## Red & Yellow
    for x in input_word_unp_unique:
        if x in goal_word_unp_unique:
            dprint(x+" is in the goal word")
            check_yellow_list.append(x)
            dprint(check_yellow_list)
        else:
            dprint(x+" is not in the goal word")
            check_red_list.append(x)
            dprint(check_red_list)
    
    ## Set Red Tags
    for i in check_red_list:
        for x in range(5):
            flag_list[input_word_unp.index(i)] = 1
            dprint(f"redtag_output_1-5: {input_word_unp.index(i)}")
        dprint(f"redtag_output: {input_word_unp.index(i)}")
    
    ## Set Yellow Tags
    for i in check_yellow_list:
        for x in range(5):
            flag_list[input_word_unp.index(i)] = 2
            dprint(f"yellowtag_output_1-5: {input_word_unp.index(i)}")
        dprint(f"yellowtag_output: {input_word_unp.index(i)}")
    
    ## Green
    for i in range(5):
        dprint(i)
        if input_word_unp[i] == goal_word_unp[i]:
            flag_list[i] = 3
    
    ## Current Progress
    dprint(goal_word_unp)
    dprint(input_word_unp)
    dprint(flag_list)

    # Format Results
    evaluated_results = ""
    for i in range(5):
        flag = flag_list[i]
        char = input_word_unp[i]
        dprint(flag)
        if flag == 0:
            dprint("no flag")
            ## Mrs Walkers suggestion/fix for not printing duplicates, replace 0 flag with whatever
            ## 1 does, worked. After changing flag 0 to print same bg color as flag 1 but different
            ## text color (aka blue instead of black) somehow, it still printed in dupes properly
            ## for both green duplicates, and dupe letters with dif flags. I have no clue how or why
            ## it fixed it, but im gratefull nomatter what, just also confused?
            
            # Found case where it fails
            ## Goal word: coded
            ## coded -> dupe green, works
            ## rotor -> dupe, dif flags. O #1 is green, works. O #2 is grey, works.
            ## cdode -> dupe D, both SHOULD be yellow. D #1 is yellow, works. D #2 is grey, doesnt
            ##   work. D #2 SHOULD also be yellow.
            
            # Mrs. Walkers sollution
            ##  Shared with me @ 11:06 AM on 9/3/2025,
            ##  (Works in 2/3 cases, ie. dupe green, dupe grey. Fails with dupe yellow):
            # {
            evaluated_results += colored(char, "blue", "on_light_grey")
            # }
        if flag == 1:
            dprint("Red")
            evaluated_results += colored(char, "black", "on_light_grey")
        if flag == 2:
            dprint("Yellow")
            evaluated_results += colored(char, "white", "on_yellow")
        if flag == 3:
            dprint("Green")
            evaluated_results += colored(char, "white", "on_green")
    
    return evaluated_results
#evaluate()

full_evaluated_results = ""

def get_valid_input(prompt, length):
    #print(debug_print)
    dprint('debug_print: '+debug_print)
    while True:
        input_word = input(prompt)
        if len(input_word) == length:
            return input_word
        else:
            print("must be",length,"letters in length")

def round_function():
    input_word = get_valid_input("Enter a 5 letter word: ",5)
    evaluated_results = evaluate(input_word)

    global full_evaluated_results
    full_evaluated_results += "\n"
    full_evaluated_results += evaluated_results

def round_display():
    if debug_noclear == 'false':
        clear_screen()
    print(full_evaluated_results)
    round_function()

def start():
    clear_screen()
    for i in range(rounds):
        print("Round "+str(rounds))
        round_display()
        #continueprompt = input("Press Enter to continue...")
    if debug_noclear == 'false':
        clear_screen()
    print(full_evaluated_results)
    print("The word was: "+goal_word)

start()

#input_word = input("Word: ")
## Stop program from exiting immediately after completetion when ran outside of IDE
exit = input('Press Enter to exit')