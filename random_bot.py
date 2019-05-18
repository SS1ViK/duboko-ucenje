import random

def random_move(board, player_sign, player_name):
    
    import tictactoe
    valid_input = False
    while not valid_input:
        turn = random.randint(-1, 8)
        if (board[turn] == ' X ') or (board[turn] == ' O '):
            continue
        else:
            valid_input = True
            board[turn] = player_sign
            tictactoe.print_board(board)

            

