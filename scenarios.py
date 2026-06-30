import pandas as pd
import os

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

# Load all paths from CSV file ONCE -> Increase performance by reading file only once and storing data
ALL_PATHS = pd.read_csv(csv_file)

def init_csv():
    # Here, we use the DataFrame() constructor and pass the "data" variable containing the dictionary as an argument to have Pandas create the Data Frame (Data Frame is a grid-like table with COLUMNS + ROWS)
    df = pd.DataFrame(data)

    # Here, we use use the "os" module and method path.exists() to check if the CSV file has been created already or not
    if not os.path.exists(csv_file):
        df.to_csv(csv_file, index=False)
    else:
        print(F"* {csv_file} * already exists, skipping export...")


def load_choices_for_path(path_name):
    # Here, we will filter the CSV file by the "Path" column based on the passed path_name
    path_df = ALL_PATHS[ALL_PATHS["Path"] == path_name]

    # 1. zip() creates an iterable tuple of two elements from the two arguments passed (which should be a pandas Series [one dimensional labled array]) -> Here, it will be the values in the "Choices" column FIRST and then the values in the "Points" column SECOND. The values will be paired by POSITION as they appear in the individual Series

    # Here, we use dict() which takes in an iterable with TWO items and converts into a dictionary -> 1.Item at index 0 (first item) is converted as the KEY 2.Item at index 1 (second item) is converted as the VALUE
    filtered_dict = dict(zip(path_df["Choices"], path_df["Points"]))
    return filtered_dict


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


def forest_path(path_name="Dark Forest"):
    """This function is executed when player selects "Dark Forest" path"""
    forest_dict = load_choices_for_path(path_name)
    print(forest_dict)


def cave_path(path_name="Mysterious Cave"):
    """This function is executed when player selects "Mysterious Cave" path"""
    cave_dict = load_choices_for_path(path_name)
    print(cave_dict)



if __name__ == "__main__":
    clear_screen()
    forest_path()
    cave_path()