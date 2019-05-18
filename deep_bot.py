import numpy as np

TRAIN_FACTOR = 0.7

def make_move(board, player_sign, player_name, all_boards):
    """
    neka le-pa funcija
    """
    #         tabla, znak,      ime,      sve table
    valid_input = False
    while not valid_input:
        import tictactoe
        if tuple(board) in all_boards:
            weights = all_boards[tuple(board)]
            turn = np.random.choice(9, p=weights/sum(weights))

        else:
            turn = np.random.choice(9)   
            all_boards[tuple(board)] = np.array([1,1,1,1,1,1,1,1,1])
            
            
        if (board[turn] == ' X ') or (board[turn] == ' O '):
            continue
        else:
            valid_input = True
            board[turn] = player_sign

def update_dict(all_boards, new_field_val, winner, first_player, board):
    
    if not all_boards:
        print("beggining, aborting...")
        return
    
    
    

    for i in range(10):
        for j in new_field_val:
            polje = all_boards[i]
            if polje[i]==new_field_val[i]:
                
                if(winner == first_player):
                    all_boards[i] += j * TRAIN_FACTOR
                else:
                    all_boards[i] -= j * TRAIN_FACTOR

