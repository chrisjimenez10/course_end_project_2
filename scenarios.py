import pandas as pd
import os
import time

# Clear screen function to clean terminal text
clear_screen = lambda: os.system("clear" if os.name == "posix" else "cls")

# Initial Data - Here, we use a dicitonary to establish COLUMNS (Keys) + ROWS (Values)
data = {
    "Path": ["Dark Forest", "Dark Forest", "Mysterious Cave", "Mysterious Cave"],
    "Choices": ["Follow River", "Climb Tree", "Light Torch", "Proceed in Darkness"],
    "Points": [200, 75, 150, 50]
}
# CSV File name -> Will be located in same directory (using relative path)
csv_file = 'game_choices.csv'

# Request from AI to generate additional choices 4x for each path
new_paths = [
    # Dark Forest - 4 new choices
    {"Path": "Dark Forest", "Choices": "Build Shelter", "Points": 125},
    {"Path": "Dark Forest", "Choices": "Track Animal Prints", "Points": 60},
    {"Path": "Dark Forest", "Choices": "Forage for Berries", "Points": 40},
    {"Path": "Dark Forest", "Choices": "Set Signal Fire", "Points": 175},
    
    # Mysterious Cave - 4 new choices
    {"Path": "Mysterious Cave", "Choices": "Check for Drafts", "Points": 90},
    {"Path": "Mysterious Cave", "Choices": "Mark Wall with Chalk", "Points": 25},
    {"Path": "Mysterious Cave", "Choices": "Listen for Echoes", "Points": 110},
    {"Path": "Mysterious Cave", "Choices": "Test Floor Stability", "Points": 180}
]


def init_csv():
    # Here, we use the DataFrame() constructor and pass the "data" variable containing the dictionary as an argument to have Pandas create the Data Frame (Data Frame is a grid-like table with COLUMNS + ROWS)
    df = pd.DataFrame(data)

    # Here, we use use the "os" module and method path.exists() to check if the CSV file has been created already or not
    if not os.path.exists(csv_file):
        df.to_csv(csv_file, index=False)
    else:
        print(F"* {csv_file} * already exists, skipping export...")


# Here, we are executing init_csv() to create CSV file for FIRST time running the program -> We MUST run this function before reading the CSV file in ALL_PATHS to prevent an error that crashes program. When this module gets imported to main.py, it will run since it is NOT inside the [ if __name__ == "__main__": ]
init_csv()
# Load all paths from CSV file ONCE -> Increase performance by reading file only once and storing data
ALL_PATHS = pd.read_csv(csv_file)

def add_paths(new_rows: list[dict[str, str | int]] | tuple[dict[str, str | int]]):
    """
    Function appends new paths as rows into existing CSV file
    Paramter "new_rows" MUST be list of dictionaries or list of tuples
    """
    new_df = pd.DataFrame(new_rows)
    if os.path.exists(csv_file):
        # Load existing CSV file
        existing_df = pd.read_csv(csv_file)
        # Append new data frame data to existing data frame -> ignore_index=True to reset row numbers and start in correct order sequence (Here we use the concat() method to concat new data frame)
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        # Write the updated data frame to the CSV file and index=False to prevent pandas from writing DataFrame index as a column in the CSV file
        updated_df.to_csv(csv_file, index=False)
        print(F"Added {len(new_df)} rows to {csv_file}")
    else:
        # Here, we handle scenario where CSV file does not exist (function runs before initiating CSV file)
        new_df.to_csv(csv_file, index=False)
        print(F"Created {csv_file} with {len(new_df)} rows")


def load_choices_for_path(path_name):
    # Here, we will filter the CSV file by the "Path" column based on the passed path_name
    path_df = ALL_PATHS[ALL_PATHS["Path"] == path_name]

    # 1. zip() creates an iterable tuple of two elements from the two arguments passed (which should be a pandas Series [one dimensional labled array]) -> Here, it will be the values in the "Choices" column FIRST and then the values in the "Points" column SECOND. The values will be paired by POSITION as they appear in the individual Series

    # Here, we use dict() which takes in an iterable with TWO items and converts into a dictionary -> 1.Item at index 0 (first item) is converted as the KEY 2.Item at index 1 (second item) is converted as the VALUE
    filtered_dict = dict(zip(path_df["Choices"], path_df["Points"]))
    return filtered_dict


def forest_path(path_name="Dark Forest"):
    """This function is executed when player selects "Dark Forest" path"""
    score:int = 0
    moves: int = 5
    choices: dict[int, str] = {
        1: "Follow River",
        2: "Climb Tree",
        3: "Build Shelter",
        4: "Track Animal Prints",
        5: "Forage for Berries",
        6: "Set Signal Fire"
    }
    forest_dict: dict[str, int] = load_choices_for_path(path_name)
    '''
    forest_dict = {
        'Follow River': 200,
        'Climb Tree': 75,
        'Build Shelter': 125,
        'Track Animal Prints': 60,
        'Forage for Berries': 40,
        'Set Signal Fire': 175
    }
    '''
    while True:
        print(F'''----- Select Choice -----
***** Moves: {moves} *****
1.Follow River
2.Climb Tree
3.Build Shelter
4.Track Animal Prints
5.Forage for Berries
6.Set Signal Fire
        ''')
        try:
            player_input = int(input("Choice: "))
            match player_input:
                case 1:
                    score += forest_dict[choices[1]]
                    print("Following the river, lookout for fresh water creatures...")
                case 2:
                    score += forest_dict[choices[2]]
                    print("Climbing the tree, are you planning to scan the area from above - Not a bad idea...")
                case 3:
                    score += forest_dict[choices[3]]
                    print("Building a shelter, are you sure building a shelter will help in finding the treasure?...")
                case 4:
                    score += forest_dict[choices[4]]
                    print("Tracking the mysterious animal, maybe they actually know where they are headed...")
                case 5:
                    score += forest_dict[choices[5]]
                    print("Foraging for berries, having fuel for this treacherous journey is a good idea...or is it?")
                case 6:
                    score += forest_dict[choices[6]]
                    print("Setting a signal fire, this light will definitely help to see the way - but what will it attract?...")
                case _:
                    clear_screen()
                    print("Invalid input, please type 1-6.")
                    continue
        except ValueError:
            clear_screen()
            print("Invalid input, please try again.")
            continue
            
        moves -= 1
        if moves <= 0:
            time.sleep(2)
            clear_screen()
            print("You have ran out of stamina and moves...")
            return score

        input("\nPress ENTER to continue...")
        clear_screen()


def cave_path(path_name="Mysterious Cave"):
    """This function is executed when player selects "Mysterious Cave" path"""
    score:int = 0
    moves: int = 5
    choices: dict[int, str] = {
        1: "Light Torch",
        2: "Proceed in Darkness",
        3: "Check for Drafts",
        4: "Mark Wall with Chalk",
        5: "Listen for Echoes",
        6: "Test Floor Stability"
    }
    cave_dict = load_choices_for_path(path_name)
    '''
    cave_dict = {
        'Light Torch': 150,
        'Proceed in Darkness': 50,
        'Check for Drafts': 90,
        'Mark Wall with Chalk': 25,
        'Listen for Echoes': 110,
        'Test Floor Stability': 180
    }
    '''
    while True:
        print(F'''----- Select Choice -----
***** Moves: {moves} *****
1.Light Torch
2.Proceed in Darkness
3.Check for Drafts
4.Mark Wall with Chalk
5.Listen for Echoes
6.Test Floor Stability
        ''')
        try:
            player_input = int(input("Choice: "))
            match player_input:
                case 1:
                    score += cave_dict[choices[1]]
                    print("Lighting the torch, the flames push back the darkness... but what else will see you now?")
                case 2:
                    score += cave_dict[choices[2]]
                    print("Proceeding in darkness, your other senses sharpen... though you can't see what hunts by sound.")
                case 3:
                    score += cave_dict[choices[3]]
                    print("Checking for drafts, a cold breeze hints at another passage... or something breathing.")
                case 4:
                    score += cave_dict[choices[4]]
                    print("Marking the wall with chalk, leaving a trail back... just hope nothing follows it.")
                case 5:
                    score += cave_dict[choices[5]]
                    print("Listening for echoes, the cave whispers back... was that water dripping, or footsteps?")
                case 6:
                    score += cave_dict[choices[6]]
                    print("Testing floor stability, each step could be your last... but fortune favors the careful.")
                case _:
                    clear_screen()
                    print("Invalid input, please type 1-6.")
                    continue
        except ValueError:
            clear_screen()
            print("Invalid input, please try again.")
            continue
            
        moves -= 1
        if moves <= 0:
            time.sleep(2)
            clear_screen()
            print("You have ran out of stamina and moves...")
            return score

        input("\nPress ENTER to continue...")
        clear_screen()
