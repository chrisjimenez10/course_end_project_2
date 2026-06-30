import sub

def start_game():
    print("Welcome to Jurassic Adventure!\nThere is a treasure awaiting, so make sure to choose wisely on the path you will take...")
    player_name = input("What is your name? ")
    player_id = sub.login_player(player_name)
    
    # sub.player_login_history(player_id=player_id)

if __name__ == "__main__":
    start_game()