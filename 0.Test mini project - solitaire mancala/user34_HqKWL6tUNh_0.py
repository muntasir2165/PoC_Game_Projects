"""
Student facing implement of solitaire version of Mancala - Tchoukaillon

Goal: Move as many seeds from given houses into the store

In GUI, you make ask computer AI to make move or click to attempt a legal move
"""


class SolitaireMancala:
    """
    Simple class that implements Solitaire Mancala
    """
    
    def __init__(self):
        """
        Create Mancala game with empty store and no houses
        """
        self._board = [0]
    
    def set_board(self, configuration):
        """
        Take the list configuration of initial number of seeds for given houses
        house zero corresponds to the store and is on right
        houses are number in ascending order from right to left
        """
        self._board = list(configuration)
    
    def __str__(self):
        """
        Return string representation for Mancala board
        """
        temp = list(self._board)
        temp.reverse()
        return str(temp)
    
    def get_num_seeds(self, house_num):
        """
        Return the number of seeds in given house on board
        """
        return self._board[house_num]

    def is_game_won(self):
        """
        Check to see if all houses but house zero are empty
        """
        for idx in range(1, len(self._board)):
            if self._board[idx] != 0:
                return False
        return True
    
    def is_legal_move(self, house_num):
        """
        Check whether a given move is legal
        """
        move_in_range = 0 < house_num < len(self._board)
        index_matches = self._board[house_num] == house_num
        return move_in_range and index_matches

    
    def apply_move(self, house_num):
        """
        Move all of the stones from house to lower/left houses
        Last seed must be played in the store (house zero)
        """
        if self.is_legal_move(house_num):  
            for idx in range(house_num):
                self._board[idx] += 1
            self._board[house_num] = 0

    def choose_move(self):
        """
        Return the house for the next shortest legal move
        Shortest means legal move from house closest to store
        Note that using a longer legal move would make smaller illegal
        If no legal move, return house zero
        """
        for house_num in range(1, len(self._board)):
            if self.is_legal_move(house_num):
                return house_num
        return 0
    
    def plan_moves(self):
        """
        Return sequence of shortest legal moves until none are available
        Not used in GUI version, only for machine testing
        """
        new_board = SolitaireMancala()
        new_board.set_board(self._board)
        move_list = []
        next_move =  new_board.choose_move()
        while next_move != 0:
            new_board.apply_move(next_move)
            move_list.append(next_move)
            next_move = new_board.choose_move()
        return move_list
 
# import test suite and run
#import poc_mancala_testsuite
#poc_mancala_testsuite.run_test(SolitaireMancala)
    
# import GUI code
#import poc_mancala_gui
#poc_mancala_gui.run_gui(SolitaireMancala())

