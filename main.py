import db_logic
import scenarios

MENU = '''
----- Menu -----
1. Play
2. Login history
3. Exit
'''
PATHS = {
    1: "Dark Forest",
    2: "Mysterious Cave"
}

def start_game():
    db_logic.init_db()

    print("Welcome to the Jurassic Adventure!\nThere is a treasure awaiting, so make sure to choose wisely on the path you will take...")
    player_name = input("What is your name? ").lower()
    scenarios.clear_screen()
    player_id = db_logic.login_player(player_name)
    total_score = 0 # Total score to determine whether player found treasure or not

    # MENU Outer Loop
    while True:
        print(MENU)
        try:
            player_input = int(input("Choice: "))
            match player_input:
                case 1: pass
                case 2:
                    scenarios.clear_screen()
                    db_logic.player_login_history(player_id=player_id)
                    continue
                case 3: return
                case _:
                    scenarios.clear_screen()
                    print(F"{player_input} is NOT a choice. Please select 1-3.")
                    continue
        except ValueError:
            scenarios.clear_screen()
            print("Invalid input, please try again.")
            continue

        # GAME LOGIC loop  
        while True:
            scenarios.clear_screen()
            print(F"Select the path you will take:\n1.{PATHS[1]}\n2.{PATHS[2]}")
            try:
                player_path_selection = int(input())
                match player_path_selection:
                    case 1:
                        total_score = scenarios.forest_path()
                        break
                    case 2:
                        total_score = scenarios.cave_path()
                        break
                    case _:
                        scenarios.clear_screen()
                        print(F"{player_path_selection} is NOT a choice. Please select 1-2.")
                        continue
            except ValueError:
                scenarios.clear_screen()
                print("Invalid input, please try again.")
                continue
            
        # WIN CONDITION -> Using total score accumulated from decisions made to determine win/lose
        if total_score >= 650:
            print("You have escaped the Dark Forest and found the treasure! Congratulations!!!")
        else:
            print("You got lost in the Dark Forest and DID NOT find the treasure...better luck next time!")
        db_logic.update_score(player_id=player_id, new_score=total_score)
        continue
            

if __name__ == "__main__":
    start_game()