"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(200)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

my_board = provided.TTTBoard(3)
#""" Example 1
my_board.move(0, 0, provided.PLAYERO)
my_board.move(0, 1, provided.PLAYERX)
my_board.move(1, 0, provided.PLAYERO)
my_board.move(1, 1, provided.PLAYERX)
my_board.move(2, 1, provided.PLAYERO)
my_board.move(2, 2, provided.PLAYERX)





#my_board.move(1, 1, provided.PLAYERX)
#my_board.move(0, 1, provided.PLAYERX)
#my_board.move(1, 0, provided.PLAYERX)
#my_board.move(0, 0, provided.PLAYERO)
#my_board.move(0, 2, provided.PLAYERO)
#my_board.move(1, 2, provided.PLAYERO)
#my_board.move(2, 0, provided.PLAYERO)
#my_board.move(2, 2, provided.PLAYERX)




#print my_board
#print my_board.check_win()
#print my_board.get_empty_squares()

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    
    #print board
    #print "winner is : ", board.check_win()
    if board.check_win() != None:
        
        return SCORES[board.check_win()] , (-1,-1)  
    
    best_score = -3* SCORES[player]
    best_move = (-1, -1) 
        
    for dummy_empty in board.get_empty_squares():
        new_board = board.clone()
        new_board.move(dummy_empty[0], dummy_empty[1], player)
        score = mm_move(new_board, provided.switch_player(player))[0]
        if score * SCORES[player]> best_score* SCORES[player]:
            
            best_score = score
            best_move = dummy_empty
            
            if score* SCORES[player] == 1:
            
                return best_score, best_move    
        
        
            
    return best_score, best_move        
    #print "score: ", score, "best_move: ", best_move    
        
    
    #return best_score, best_move

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
#print mm_move(my_board, provided.PLAYERX)
#print mm_move(provided.TTTBoard(3, False, [[provided.EMPTY, provided.PLAYERX, provided.EMPTY], [provided.PLAYERO, provided.PLAYERX, provided.EMPTY], [provided.PLAYERO, provided.EMPTY, provided.EMPTY]]), provided.PLAYERO)
#MYBOARD1 = provided.TTTBoard(3, False, [[provided.PLAYERO, provided.PLAYERX, provided.PLAYERX], [provided.EMPTY, provided.PLAYERX, provided.PLAYERO], [provided.PLAYERX, provided.PLAYERO, provided.PLAYERX]])
#print "start\n", MYBOARD1

#score_final, move_final = mm_move(MYBOARD1, provided.PLAYERO)
#print "score, move final:", score_final, move_final
#print mm_move(provided.TTTBoard(3, False, [[provided.PLAYERX, provided.PLAYERX, provided.PLAYERO], [provided.EMPTY, provided.PLAYERX, provided.PLAYERX], [provided.PLAYERO, provided.EMPTY, provided.PLAYERO]]), provided.PLAYERO)
provided.play_game(move_wrapper, 1, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
