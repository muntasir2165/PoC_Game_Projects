"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        #check if ile zero is positioned at (i,j)
        if self.get_number(target_row, target_col) != 0 :
            return False
        
        #check if all tiles in rows i+1 or below are positioned at their solved location
        puzzle_width = self.get_width()
        puzzle_height = self.get_height()
        for row in range(target_row+1, puzzle_height):
            for column in range(puzzle_width):
                if self.get_number(row, column) != (column + puzzle_width * row):
                    return False
        
        #check if all tiles in row i to the right of position (i,j)
        #are positioned at their solved location
        for column in range(target_col+1, puzzle_width):
            if self.get_number(target_row, column) != (column + puzzle_width * target_row):
                return False
        
        #if all the above checks pass, then return True    
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        # replace with your code
        puzzle_copy = self.clone()
        target_number = target_col + puzzle_copy.get_width() * target_row
        current_target_position = self.current_position(target_row, target_col)
        move_string = ""
        
        #case 1: target tile above zero tile (different row same column)
        if (current_target_position[1] == target_col) and (current_target_position[0] != target_row):
            move_string += "u" * (target_row - current_target_position[0])
            puzzle_copy.update_puzzle(move_string)
            
            while (puzzle_copy.get_number(target_row, target_col) != target_number):
                move_string += "lddru"
                puzzle_copy.update_puzzle("lddru")
            move_string += "ld"
            
        #case 2: target tile to the left of zero tile (same row different column)
        elif (current_target_position[0] == target_row) and (current_target_position[1] <= target_col):
            #print "recursive loop", current_target_position
            move_string = "l" * (self.current_position(0, 0)[1] - current_target_position[1])
            #print move_string
            puzzle_copy.update_puzzle(move_string)
            
            while (puzzle_copy.get_number(target_row, target_col) != target_number):
                current_move_string = "u" + "r" * (target_col - current_target_position[1]) + "d"
                current_target_position = puzzle_copy.current_position(target_row, target_col)
                current_move_string += "l" * (target_row - current_target_position[1])
                puzzle_copy.update_puzzle(current_move_string)
                move_string += current_move_string
                
        #case 3: else (two scenarios: target tile is at the north west or north east of zero tile)
        #(different row different column)
        elif (current_target_position[0] != target_row) and (current_target_position[1] != target_col):
            #target tile is at the north west
            if current_target_position[1] <= target_col:
                move_string = "l" * (target_col - current_target_position[1]) + "u" * (target_row - current_target_position[0])
            puzzle_copy.update_puzzle(move_string)
            
            while (puzzle_copy.current_position(target_row, target_col)[0] != target_row):
                current_move_string = "r" + "d" * (target_row - current_target_position[0]) + "l"
                current_target_position = puzzle_copy.current_position(target_row, target_col)
                current_move_string += "u" * (target_row - current_target_position[0])
                puzzle_copy.update_puzzle(current_move_string)
                move_string += current_move_string
            move_string += "rd"
            puzzle_copy.update_puzzle("rd")
            #print "copy puzzle:\n", puzzle_copy
            #print target_row, puzzle_copy.current_position(target_row, target_col)
            more_moves = puzzle_copy.solve_interior_tile(target_row, target_col)
            move_string += more_moves
            
            '''
            #target tile is at the north east
            elif current_target_position[1] >= target_col:
                move_string = "r" * (target_col - current_target_position[1]) + "u" * (target_row - current_target_position[0])
            puzzle_copy.update_puzzle(move_string)
            
            while (puzzle_copy.current_position(target_row, target_col)[0] != target_row):
                current_move_string = "l" + "d" * (target_row - current_target_position[0]) + "r"
                current_target_position = puzzle_copy.current_position(target_row, target_col)
                current_move_string += "u" * (target_row - current_target_position[0])
                puzzle_copy.update_puzzle(current_move_string)
                move_string += current_move_string
            move_string += "ld"
            puzzle_copy.update_puzzle("ld")
            more_moves = puzzle_copy.solve_interior_tile(target_row, target_col)
            move_string += more_moves
            '''
        self.update_puzzle(move_string)
        #print "actual puzzle:\n", self
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        #check if ile zero is positioned at (i,j)
        if self.get_number(0, target_col) != 0 :
            return False
        
        #check if all tiles in from column j and below (more precisely, from (1, j) and below)
        #are positioned at their solved location
        puzzle_width = self.get_width()
        puzzle_height = self.get_height()
        
        #check for row 1
        for column in range(target_col, puzzle_width):
            if self.get_number(1, column) != (column + puzzle_width * 1):
                    return False
                
        for row in range(2, puzzle_height):
            for column in range(puzzle_width):
                if self.get_number(row, column) != (column + puzzle_width * row):
                    return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        #check if ile zero is positioned at (i,j)
        if self.get_number(1, target_col) != 0 :
            return False
        
        #check if all tiles in from column j and below (more precisely, from (1, j+1) and below)
        #are positioned at their solved location
        puzzle_width = self.get_width()
        puzzle_height = self.get_height()
        
        #check for row 1
        for column in range(target_col+1, puzzle_width):
            if self.get_number(1, column) != (column + puzzle_width * 1):
                    return False
                
        for row in range(2, puzzle_height):
            for column in range(puzzle_width):
                if self.get_number(row, column) != (column + puzzle_width * row):
                    return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        puzzle_copy = self.clone()
        #check if tile zero is positioned at (0,0)
        if puzzle_copy.get_number(0, 0) != 0:
            zero_position = puzzle_copy.current_position(0, 0)
        move_string = ("l" * zero_position[0]) + ("u" * zero_position[1])
        puzzle_copy.update_puzzle(move_string)
        
        while not(puzzle_copy.get_number(0, 0) == 0 and puzzle_copy.get_number(0, 1) == 1 and puzzle_copy.get_number(1, 0) == (0 + puzzle_copy.get_width() * 1) and puzzle_copy.get_number(1, 1) == (1 + puzzle_copy.get_width() * 1)):
            move_string += "rdlu"
            puzzle_copy.update_puzzle("rdlu")
        
        self.update_puzzle(move_string)
        return move_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        return ""

# Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4, [[4, 13, 1, 3], [5, 10, 2, 7], [8, 12, 6, 11],[9, 0, 14, 15]]))

#phase 1 testing
#solve_interior_tile() case 1
#puzzle = Puzzle(4, 4, [[4, 13, 1, 3], [5, 10, 2, 7], [8, 12, 6, 11],[9, 0, 14, 15]])
#poc_fifteen_gui.FifteenGUI(puzzle)
#puzzle.solve_interior_tile(3, 1)

#solve_interior_tile() case 2
#puzzle = Puzzle(4, 4, [[6, 7, 8, 9], [2, 3, 4, 5], [10, 1, 0, 11],[12, 13, 14, 15]])
#poc_fifteen_gui.FifteenGUI(puzzle)
#print "llurrdll"
#puzzle.solve_interior_tile(2, 2)

#solve_interior_tile() case 3
#puzzle = Puzzle(4, 4, [[10, 6, 7, 1], [5, 4, 3, 2], [9, 8, 0, 11],[12, 13, 14, 15]])
#poc_fifteen_gui.FifteenGUI(puzzle)
#print "lluurddluu"
#puzzle.solve_interior_tile(2, 2)

#solve_interior_tile() case 3
#puzzle = Puzzle(4, 4, [[1, 6, 7, 10], [5, 4, 3, 2], [9, 8, 0, 11],[12, 13, 14, 15]])
#poc_fifteen_gui.FifteenGUI(puzzle)
#puzzle.solve_interior_tile(2, 2)

#puzzle = Puzzle(4, 4, [[4, 13, 1, 3], [5, 10, 2, 7], [8, 12, 6, 11],[0, 13, 14, 15]])
#poc_fifteen_gui.FifteenGUI(puzzle)
#puzzle.update_puzzle("uuu")

#phase 3 testing
#obj = Puzzle(3, 3, [[4, 3, 2], [1, 0, 5], [6, 7, 8]])
#obj.solve_2x2()


