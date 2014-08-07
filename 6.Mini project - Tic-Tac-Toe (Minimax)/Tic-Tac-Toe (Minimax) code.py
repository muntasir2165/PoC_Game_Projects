"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    #completed board case
    no_more_moves = board.check_win()
    if (no_more_moves != None):
        return SCORES[no_more_moves], (-1, -1) 
    else:
        score_move_list = []
        empty_squares = board.get_empty_squares()
        for next_move in empty_squares:
            board_copy = board.clone()
            board_copy.move(next_move[0], next_move[1], player)
            #case where the game ends after the above move
            is_game_over = board_copy.check_win()
            if (is_game_over != None):
                return SCORES[is_game_over], next_move
            else:
                next_player = provided.switch_player(player)
                score= mm_move(board_copy, next_player)[0]
                score_move_list.append((score, next_move))
        #sort the list for scoring purposes
        score_move_list.sort()
        if player == provided.PLAYERX:
            best_score = score_move_list[-1][0]
            best_move = score_move_list[-1][1]
        if player == provided.PLAYERO:
            best_score = score_move_list[0][0]
            best_move = score_move_list[0][1]
        return best_score, best_move
                

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
