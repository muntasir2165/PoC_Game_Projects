"""
Implementation of SolitaireMancala class for the game
of the same name
"""
class SolitaireMancala:
    """
    Class that implements Solitaire Mancala
    """
    
    def __init__(self):
        """
        Create Mancala game with only an empty store
        and no houses
        """
        self._board = [0]
        
    def set_board(self, configuration):
        """
        Create a mancala board game with the given
        configuration of seeds in the houses. The store
        (to the right in the actual board) is the first
        entry and the rest are houses from right  to 
        left in ascending order
        """
        self._board = list(configuration)
        
    def __str__(self):
        """
        Return a string corresponding to the current
        configuration of the Mancala board. This string
        is formatted as a list with the store appearing
        in the rightmost (last) entry.
        """
        board = list(self._board)
        board.reverse()
        return str(board)
    
    def get_num_seeds(self, house_num):
        """
        Return the number of seeds in the house with
        index house_num. Note that house 0 corresponds
        to the store.
        """
        if (0 <= house_num and house_num < len(self._board)):
           return self._board[house_num]
    
    def is_legal_move(self, house_num):
        """ Return True if moving the seeds from house house_num is legal.
        Otherwise, return False. If house_num is zero, is_legal_move
        should return False"""
        if (1 <= house_num and house_num < len(self._board)):
            if house_num == self._board[house_num]:
                return True
            else:
                return False
        else:
            return False
        
    def apply_move(self, house_num):
        """ Apply a legal move for house house_num to the board."""
        if self.is_legal_move(house_num):
            for idx in range(house_num):
                self._board[idx] += 1
            self._board[house_num] = 0
        
    def choose_move(self):
        """ Return the index for the legal move whose house is
        closest to the store. If no legal move is available, return 0."""
        for idx in range(1, len(self._board)):
            if self.is_legal_move(idx):
                return idx
        return 0
    
    def is_game_won(self):
        """Return True if all houses contain no seeds.
        Return False otherwise."""
        count = 0
        for idx in range(len(self._board)-1, 0, -1):
            count += self._board[idx]
            
        if count == 0:
            return True
        else:
            return False
        
    def plan_moves(self):
        """Given a Mancala game, return a list of legal moves
        computed to win the game if possible. In computing this
        sequence, the method repeatedly chooses the move whose
        house is closest to the store when given a choice of
        legal moves."""
        legal_moves = []
        game = SolitaireMancala()
        game.set_board(list(self._board))
        next_move = game.choose_move()
        while (next_move != 0):
            game.apply_move(next_move)
            legal_moves.append(next_move)
            next_move = game.choose_move()
        return legal_moves
  
#import test suite and run
#import poc_mancala_testsuite
#poc_mancala_testsuite.run_test(SolitaireMancala)

#import poc_mancala_gui
#poc_mancala_gui.run_gui(SolitaireMancala())