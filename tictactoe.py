import os
import random_bot as rb
import deep_bot as db
import pickle
C_ROWS = 3
C_COLS = 3
EMPTY_SYMBOL = ' - '
DIR_PATH = "results"
FILE_EXTENSION = ".txt"

BOARD_FIELDS = {
    (0, 0) : 0,
    (0, 1) : 1,
    (0, 2) : 2,
    
    (1, 0) : 3,
    (1, 1) : 4,
    (1, 2) : 5,
    
    (2, 0) : 6,
    (2, 1) : 7,
    (2, 2) : 8
}

def display_welcome_message():
    """
    Displays welcome message for the players.
    """
    print("Welcome to the awesome tick-tack-toe game simulator, I hope you'll have fun!")

def get_player_names():
    """
    Gets and returns player names as a tuple.
    First element in the tuple is the name of the first player.
    Second element in the tuple is the name of the second player.
    """
    first_player = input("Please input the name of the first player: ")

    second_player = input("Please input the name of the second player: ")

    return first_player, second_player

def construct_board():
    """
    Creates empty tick-tack-toe board
    It returns it as a matrix of strings.
    """


    board = []
    
    i = 0
    while i < C_ROWS * C_COLS:
        board.append(EMPTY_SYMBOL)
        i += 1

    return board

def create_signs(first_player, second_player):
    """
    Creates and returns dictionary which contains signs which players are using,
    it can be modifed to take custom signs.
    """

    signs = {}
    signs[first_player] = " X "  
    signs[second_player] = " O "

    return signs

def print_board(board):
    """
    Prints the current board.
    """


    i = 0
    j = 0

    to_print = ""
    while i < C_COLS * C_ROWS:
        
        to_print += board[i]
        j += 1
        
        if j == 3:
            to_print += "\n"
            j = 0        
        
        i += 1

    print(to_print)

def make_input(board, player, player_sign):
    """
    Asks the player for input, check if the input is correct and update the board if it is.
    Returns the col and row players has input
    """
    valid_fields = ['0', '1', '2']

    
    print(player, " on the move")

    valid_input = False
    while not valid_input:

        player_input = input("Please input row and column, separated by space: ")
        player_input = player_input.split(" ")
        
        if len(player_input) != 2: 
            print("You must enter 2 valid fields separated by space, try again")
            continue
        
        row = player_input[0]
        col = player_input[1]

        if row not in valid_fields or col not in valid_fields:
            print("You must enter 2 valid fields, try again")
            continue
        
        row = int(row)
        col = int(col)

        if board[BOARD_FIELDS[(row, col)]] != EMPTY_SYMBOL:
            print("That field already has an input, try again")
            continue
        
        valid_input = True
        board[BOARD_FIELDS[(row, col)]] = player_sign
        
    print_board(board)

def tie(board):
    """
    Checks if the result is tied. This function is always called after
    win checking, so that we for sure know that there are no more fields to be filled
    and that no one has won
    """
    all_filled = True
    
    for field in BOARD_FIELDS.values():
        if board[field] == EMPTY_SYMBOL:
            all_filled = False

    return  all_filled

def check_win(board, sign):
    """
    Checks if the player who had last input has won, returns true or false
    """
    if board[0] == board[1] == board[2] == sign:
        return True
    
    if board[3] == board[4] == board[5] == sign:
        return True
    
    if board[6] == board[7] == board[8] == sign:
        return True

    if board[0] == board[3] == board[6] == sign:
        return True
    
    if board[1] == board[4] == board[7] == sign:
        return True

    if board[2] == board[5] == board[8] == sign:
        return True

    if board[0] == board[4] == board[8] == sign:
        return True

    if board[2] == board[4] == board[6] == sign:
        return True

    return False

def create_file_path(first_player, second_player):
    """
    Creates appropriate file path as stated in the specification
    
    File path is: first_player + second_player + FILE_EXTENSION 
    
    Returns that file as a string.
    """
    file_name = first_player.lower() + second_player.lower() + FILE_EXTENSION
    file_path = os.path.join(DIR_PATH, file_name)
    return file_path

def record_result(first_player, second_player, winner):
    """
    Records the result for the current game. Tries to write into the 
    file which is named first_player_second_player and which is stored in
    the directory results. 
    
    If the file with the same name (or with the inverted name) exists, it writes into 
    that file, otherwise makes a new file. 
    
    File name is all lower case.
    """
    file_path = create_file_path(first_player, second_player)

    first_player_won = 0
    second_player_won  = 0
    tie = 0

    if winner == first_player:
            first_player_won += 1
        
    elif winner == second_player:
        second_player_won += 1
        
    else:
        tie += 1

    
    if os.path.isfile(file_path):
        data = open(file_path, 'r+')
        games_data = data.readlines()
        first_player_wins = int(games_data[0])
        second_player_wins = int(games_data[1])
        ties = int(games_data[2])
        data.close()

        
        data = open(file_path, "w")
        data.write(str(first_player_wins + first_player_won) + "\n")
        data.write(str(second_player_wins + second_player_won) + "\n")
        data.write(str(ties + tie) + "\n")
        data.close()


    else:
        data = open(file_path, "w")
        data.writelines(str(first_player_won) + "\n")
        data.writelines(str(second_player_won) + "\n")
        data.writelines(str(tie) + "\n")
        data.close()

def display_current_stats(first_player, second_player):
    """
    Opens the file for the players, and reads displays the game data following format:
    - Number of wins for the first player, win percentage of the first player
    - Number of wins for the second player, win percentage of the second player
    - Number of tied games, tie games percentage
    """
    file_path = create_file_path(first_player, second_player)
    data = open(file_path, "r")
    
    games_data = data.readlines()
    data.close()

    first_player_wins = int(games_data[0])
    second_player_wins = int(games_data[1])
    tied_games = int(games_data[2])

    all_games = first_player_wins + second_player_wins + tied_games

    first_player_percentage = round(first_player_wins / all_games, 2) * 100
    second_player_percentage = round(second_player_wins / all_games, 2) * 100 
    tied_games_percentage = round(tied_games / all_games, 2) * 100

    print("First player wins:", first_player_wins, ",", first_player_percentage, "% of all games") 
    print("Second player wins:", second_player_wins, ",", second_player_percentage, "% of all games") 
    print("Tied games:", tied_games, ",", tied_games_percentage, "% of all games") 

def ask_for_another_game():
    """
    Asks the players if they want to play another game.
    
    Returns true if they want, false otherwise
    """
    valid_answers = ["y", "n"]
    answer = ""
    
    while answer not in valid_answers:
        print("Do you want to play another game [y / n]?")
        answer = input()
    
    if answer.lower() == "y":
        print("Starting a new game!")
        return True
    else:
        print("Goodbye, thanks for playing!")
        return False

def main():    
    
    display_welcome_message()
    first_player, second_player = get_player_names()
    #playing_again = True
    new_field_val={}
    all_boards={}
    #while playing_again:
    while True:
        board = construct_board()
        winner = ""    
        signs = create_signs(first_player, second_player)
        with open("dict.pickle","rb") as pickle_in:
            all_boards=pickle.load(pickle_in)   
        first_player_move = True
                                    
        while not tie(board) and winner == "":
            if first_player_move:
                #rb.random_move(board, signs[first_player], first_player)
                #make_input(board, first_player, signs[first_player])
                db.make_move(board, signs[first_player], first_player, all_boards)
                if check_win(board, signs[first_player]):
                    winner = first_player
                
                first_player_move = False
            else:
                #db.make_move(board, signs[second_player], second_player, field_val, new_field_val, all_boards)
                rb.random_move(board, signs[second_player], second_player)
                #make_input(board, second_player, signs[second_player])
                if check_win(board, signs[second_player]):
                    winner = second_player
                
                first_player_move = True
                
            
        if winner == "":
            print("It's a tie!")      
        else:
            print("Winner is: ", winner)
        record_result(first_player, second_player, winner)
        display_current_stats(first_player, second_player)
        db.update_dict(all_boards, new_field_val, winner, first_player, board)
        pickle_out = open("dict.pickle","wb")
        pickle.dump(all_boards, pickle_out)
        pickle_out.close()
        #playing_again = ask_for_another_game()

if __name__ == "__main__":
    main()
