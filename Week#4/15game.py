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
        # replace with your code
        if self._grid[target_row][target_col] == 0:
            
            for col in range(target_col+1, self._width):
                
                correct_value = col + self._width * target_row 
                if self._grid[target_row][col] != correct_value:
                    return False
            if target_row != self._height - 1:    
                for col in range(self._width):
                    correct_value = col + self._width * (target_row + 1)
                    if self._grid[target_row + 1][col] != correct_value:
                        return False
             
            return True
        
        else:
            return False
        
        

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        # replace with your code
        moving_string = ""
        
        tar_til_row, tar_til_col = self.current_position(target_row, target_col)
         
        
        # moving zero tile  upward to the target tile
        for dummy_idx in range(tar_til_row, target_row):
                
                moving_string += "u"
        
        #if the target tile is in the same column as zero tile
        if tar_til_col == target_col:
            for dummy_idx1 in range(tar_til_row, target_row - 1):
                
                moving_string += "lddru"
        
        else:
            
            if tar_til_col > target_col:
                
                for dummy_idx1 in range(target_col , tar_til_col):
                    moving_string += "r" 
                
                if tar_til_row == 0:
            
                    
                    for dummy_idx1 in range(target_col ,tar_til_col - 1):
                        moving_string += "dllur"
                    
                    moving_string += "dlu"
                    for dummy_idx1 in range(tar_til_row, target_row - 1):
                
                        moving_string += "lddru"
                    
                else:    
                    for dummy_idx1 in range(target_col ,tar_til_col - 1):
                        moving_string += "ulldr"
                    
                    moving_string += "ul"
                    for dummy_idx1 in range(tar_til_row, target_row):
                
                        moving_string += "lddru"

            
            elif tar_til_col < target_col:
                
                for dummy_idx1 in range(tar_til_col , target_col):
                    moving_string += "l"
                
                if tar_til_row == 0:
                    
                    for dummy_idx1 in range(tar_til_col + 1 ,target_col):
                        moving_string += "drrul"
                    
                    moving_string += "dru"
                    for dummy_idx1 in range(tar_til_row, target_row - 1):
                        
                        moving_string += "lddru"
                    
                
                else:
                    
                    for dummy_idx1 in range(tar_til_col + 1 ,target_col):
                        moving_string += "urrdl"
                    
                    moving_string += "ur"    
                    
                    for dummy_idx1 in range(tar_til_row, target_row):
                        
                        moving_string += "lddru"


        moving_string += "ld"
        
        self.update_puzzle(moving_string)
        return moving_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # replace with your code
        moving_string = ""
        
        tar_til_row, tar_til_col = self.current_position(target_row, 0)
        
        if tar_til_row == target_row - 1 and tar_til_col == 0:
            moving_string += "u"
            for dummy_idx in range(self._width -1):
                moving_string += "r"
            self.update_puzzle(moving_string)
            return moving_string
        
        else:
            
            for dummy_idx in range(tar_til_row, target_row):
                moving_string += "u"
            
            for dummy_idx1 in range(0 , tar_til_col):
                    moving_string += "r"
            
            if tar_til_col == 0:
                    moving_string += "drul"
            
            else:
                
                if tar_til_row == 0:
                                
                    for dummy_idx1 in range(0 ,tar_til_col - 1):
                        moving_string += "dllur"
                else:
                                    
                    for dummy_idx1 in range(0 ,tar_til_col - 1):
                            moving_string += "ulldr"
                        
                moving_string += "l"
            for dummy_idx1 in range(tar_til_row, target_row - 1):
                moving_string += "druld"
       
        
        moving_string += "ruldrdlurdluurddlur"
        for dummy_idx in range(1,self._width -1):
            moving_string += "r"
            
            
        self.update_puzzle(moving_string)
        return moving_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        
        if self._grid[0][target_col] == 0:
            
            for col in range(target_col+1, self._width):
                
                correct_value = col + self._width * 0 
                if self._grid[0][col] != correct_value:
                    
                    return False
            
            for col in range(target_col, self._width):
                
                correct_value = col + self._width * 1 
                if self._grid[1][col] != correct_value:
                    
                    return False
                
            for col in range(self._width):
                for row in range(2, self._height):
                
                    correct_value = col + self._width * row 
                    if self._grid[row][col] != correct_value:
                        
                        return False    
            return True
        
        else:
            return False
        

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        
        if self._grid[1][target_col] == 0:
            
            for col in range(target_col + 1, self._width):
                
                correct_value = col + self._width * 1 
                if self._grid[1][col] != correct_value:
                    
                    return False
                
            for col in range(self._width):
                for row in range(2, self._height):
                
                    correct_value = col + self._width * row 
                    if self._grid[row][col] != correct_value:
                        
                        return False            
             
            return True
        
        else:
            return False

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        moving_string = "ld"
        
        tar_til_row, tar_til_col = self.current_position(0, target_col)
             
        
        if tar_til_row == 0 and tar_til_col == target_col - 1:
            self.update_puzzle(moving_string)
            return moving_string
        
        if tar_til_row == 1 and tar_til_col == target_col - 1:
            moving_string += "uld"
            moving_string += "urdlurrdluldrruld"
            self.update_puzzle(moving_string)
            return moving_string
        
        for dummy_idx1 in range(tar_til_col , target_col - 1):
                moving_string += "l"
        
        if tar_til_row == 0 :
            
            for dummy_idx in range(tar_til_col , target_col - 1):
                moving_string += "ruldr"
            
            moving_string += "uld"    
        
        else:
            
            for dummy_idx in range(tar_til_col , target_col - 2):
                moving_string += "urrdl"
            
            
        moving_string += "urdlurrdluldrruld"
                
        
        self.update_puzzle(moving_string)
        return moving_string
        
    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        moving_string = ""
        
        tar_til_row, tar_til_col = self.current_position(1, target_col)
         
        
        # moving zero tile  upward to the target tile
        for dummy_idx in range(tar_til_row, 1):
                
                moving_string += "u"
        
        #if the target tile is in the same column as zero tile
        if tar_til_col == target_col:
            
            self.update_puzzle(moving_string)
            return moving_string
        
        
        else:
            
            for dummy_idx1 in range(tar_til_col , target_col):
                moving_string += "l"
            
            if tar_til_row == 0:
                for dummy_idx1 in range(tar_til_col + 1 ,target_col):
                    moving_string += "drrul"
                moving_string += "dru"
                
            else:
                for dummy_idx1 in range(tar_til_col + 1 ,target_col):
                    moving_string += "urrdl"
                moving_string += "ur"    

        
        self.update_puzzle(moving_string)
        return moving_string


    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        moving_string = "ul"
        self.update_puzzle("ul")
        
        tar_til_row, tar_til_col = self.current_position(0, 1)
        
        while(tar_til_row != 0 or tar_til_col != 1):
            moving_string += "rdlu"
            
            self.update_puzzle("rdlu")
            tar_til_row, tar_til_col = self.current_position(0, 1)
            
        
        return moving_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        moving_string = ""
        zero_row , zero_col = self.current_position(0, 0)
        
        done = False
        
        for row in range(self._height - 1, -1, -1):
            for col in range(self._width - 1 , -1, -1):
                
                if (self.current_position(row, col)) != (row,col):
                    
                    for dummy_idx in range(abs(col-zero_col)):
                        
                        if col <= zero_col:
                            moving_string += "l"
                        elif col > zero_col:
                            moving_string += "r"
                            
                            
                    for dummy_idx in range(abs(row-zero_row)):
                        moving_string += "d"
                    done = True
                    break
            if done:
                break
                    
        self.update_puzzle(moving_string)
        
        for row in range(self._height - 1, 1, -1):
            for col in range(self._width - 1 , -1, -1):
                #tar_row, tar_col = self.current_position(row, col)
                if (self.current_position(row, col)) != (row,col):
                    
                    if col == 0 :
                        assert self.lower_row_invariant(row, col)
                        moving_string += self.solve_col0_tile(row)
                    else:    
                    
                        assert self.lower_row_invariant(row, col)
                        moving_string +=self.solve_interior_tile(row, col)
                    
        
        for col in range(self._width - 1, 1, -1):
            
            if (self.current_position(1, col)) != (1,col):
                assert self.row1_invariant(col)
                moving_string += self.solve_row1_tile(col)
            
            if (self.current_position(0, col)) != (0,col):            
                assert self.row0_invariant(col)
                moving_string += self.solve_row0_tile(col)
                     
                assert self.row1_invariant(col - 1)
        
        if (self.current_position(0, 0)) == (0,0) and (self.current_position(0, 1)) == (0,1):
            pass
        else: moving_string += self.solve_2x2()
        return moving_string

# Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4, [[4, 13, 1, 3], [5, 10, 2, 7], [8, 12, 6, 11], [9, 14, 15, 0]]))
#my_puzzle = Puzzle(4, 4, [[4, 1, 3, 9], [5, 10, 2, 7], [8, 0, 6, 11], [13, 12, 14, 15]])
#print my_puzzle
#my_puzzle.solve_interior_tile(2, 1)
#print my_puzzle
#poc_fifteen_gui.FifteenGUI(Puzzle(3, 3, [[2,4,0], [3,1,7], [6,5,8]]))
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))
#my_puzzle = Puzzle(3, 3, [[1, 4, 2], [6, 0, 8], [3, 7, 5]])
#print my_puzzle
#my_puzzle.solve_interior_tile(2,2)
#print my_puzzle
#my_puzzle.solve_interior_tile(2,1)
#print my_puzzle
#my_puzzle.solve_interior_tile(2,0)
#print my_puzzle

#my_puzzle = Puzzle(4, 4, [[4, 13, 1, 3], [5, 10, 2, 7], [8, 12, 6, 11], [9, 14, 0, 15]])
#my_puzzle =  Puzzle(3, 3, [[0, 1, 2], [3, 4, 5], [6, 7, 8]])
#my_puzzle =  Puzzle(3, 6, [[16, 7, 13, 17, 5, 9], [3, 0, 14, 10, 12, 6], [4, 15, 2, 11, 8, 1]])
#print my_puzzle
#print my_puzzle.solve_puzzle()
#print my_puzzle
#poc_fifteen_gui.FifteenGUI(Puzzle(3, 6, [[16, 7, 13, 17, 5, 9], [3, 0, 14, 10, 12, 6], [4, 15, 2, 11, 8, 1]]))
#my_puzzle = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#print my_puzzle
#my_puzzle.solve_puzzle()
#print my_puzzle
#my_puzzle.solve_2x2()
#my_puzzle.solve_col0_tile(3)
#print my_puzzle
#my_puzzle.solve_interior_tile(3, 0)
#print my_puzzle
#my_puzzle.solve_interior_tile(2, 2)
#print my_puzzle
my_puzzle =  Puzzle(6,6, [[1,2,3,4,5,6],[7,8,9,10,11,12],[13,14,15,16,17,18],[19,20,21,22,23,24],[25,26,27,28,29,30],[31,32,33,34,35,36]])
poc_fifteen_gui.FifteenGUI(Puzzle(6,6, [[1,2,3,4,5,6],[7,8,0,10,11,12],[13,14,15,16,17,18],[19,20,21,22,23,24],[25,26,27,28,29,30],[31,32,33,34,35,9]]))
