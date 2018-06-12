"""
Student facing code for Tantrix Solitaire
http://www.jaapsch.net/puzzles/tantrix.htm

Game is played on a grid of hexagonal tiles.
All ten tiles for Tantrix Solitaire and place in a corner of the grid.
Click on a tile to rotate it.  Cick and drag to move a tile.

Goal is to position the 10 provided tiles to form
a yellow, red or  blue loop of length 10
"""



# Core modeling idea - a triangular grid of hexagonal tiles are 
# model by integer tuples of the form (i, j, k) 
# where i + j + k == size and i, j, k >= 0.

# Each hexagon has a neighbor in one of six directions
# These directions are modeled by the differences between the 
# tuples of these adjacent tiles

# Numbered directions for hexagonal grid, ordered clockwise at 60 degree intervals
DIRECTIONS = {0 : (-1, 0, 1), 1 : (-1, 1, 0), 2 : (0, 1, -1), 
              3 : (1, 0, -1), 4 : (1, -1, 0), 5 : (0,  -1, 1)}

def reverse_direction(direction):
    """
    Helper function that returns opposite direction on hexagonal grid
    """
    num_directions = len(DIRECTIONS)
    return (direction + num_directions / 2) % num_directions



# Color codes for ten tiles in Tantrix Solitaire
# "B" denotes "Blue", "R" denotes "Red", "Y" denotes "Yellow"
SOLITAIRE_CODES = ["BBRRYY", "BBRYYR", "BBYRRY", "BRYBYR", "RBYRYB",
                "YBRYRB", "BBRYRY", "BBYRYR", "YYBRBR", "YYRBRB"]


# Minimal size of grid to allow placement of 10 tiles
MINIMAL_GRID_SIZE = 4



class Tantrix:
    """
    Basic Tantrix game class
    """
    
    def __init__(self, size):
        """
        Create a triangular grid of hexagons with size + 1 tiles on each side.
        """
        assert size >= MINIMAL_GRID_SIZE
        self._tile_value = {}
        self._size = size
        counter = 0
        for dummy_k in range(self._size, -1, -1):
            for dummy_i in range(self._size):
                for dummy_j in range(self._size):
                    if (dummy_i + dummy_j == self._size - dummy_k):
                        
                        if counter < len(SOLITAIRE_CODES):
                            self._tile_value[(dummy_i, dummy_j, dummy_k)] = SOLITAIRE_CODES[counter]
                            
                        counter += 1    
            
        

        # Initialize dictionary tile_value to contain codes for ten
        # tiles in Solitaire Tantrix in one 4x4 corner of grid
        

    def __str__(self):
        """
        Return string of dictionary of tile positions and values
        """
        return str(self._tile_value)
        
    def get_tiling_size(self):
        """
        Return size of board for GUI
        """
        return self._size
    
    def tile_exists(self, index):
        """
        Return whether a tile with given index exists
        """
        return (index in self._tile_value) 
    
    def place_tile(self, index, code):
        """
        Play a tile with code at cell with given index
        """
        self._tile_value[index] = code        

    def remove_tile(self, index):
        """
        Remove a tile at cell with given index
        and return the code value for that tile        """
        return self._tile_value.pop(index)
               
    def rotate_tile(self, index):
        """
        Rotate a tile clockwise at cell with given index
        """
        cur_code = self._tile_value[index]
        self._tile_value[index] = cur_code[-1] + cur_code[:-1]

    def get_code(self, index):
        """
        Return the code of the tile at cell with given index
        """
        return self._tile_value[index]

    def get_neighbor(self, index, direction):
        """
        Return the index of the tile neighboring the tile with given index in given direction
        """
        neigh_idx = tuple( index[dim] + DIRECTIONS[direction][dim] for dim in range(3))
        return neigh_idx

    def is_legal(self):
        """
        Check whether a tile configuration obeys color matching rules for adjacent tiles
        """
        
        for tile in self._tile_value:
            legal = False
            for direct in DIRECTIONS:
                neigh = self.get_neighbor(tile, direct)
                if neigh in self._tile_value:
                    neigh_edge = reverse_direction(direct)
                    if self._tile_value[tile][direct] == self._tile_value[neigh][neigh_edge]:
                        legal = True
                    else:
                        legal = False
                        return legal

        return legal
            
    def has_loop(self, color):
        """
        Check whether a tile configuration has a loop of size 10 of given color
        """
        if not self.is_legal():
            return False
        
        tile_indecis = self._tile_value.keys()
        start_index = tile_indecis[0]
        
        start_tile = self._tile_value[start_index]
        
        next_direction = 0 
        
        for dummy_idx in range(6):
            if start_tile[dummy_idx] == color and (self.get_neighbor(start_index, dummy_idx) not in self._tile_value):
                return False
        
        for dummy_idx in range(6):
            if start_tile[dummy_idx] == color:
                next_direction = dummy_idx
                break
 
        next_index = self.get_neighbor(start_index, next_direction)
        
        current_len = 1
        
        while start_index != next_index:
            print next_index
            current_index = next_index
            current_tile = self._tile_value[current_index]
            current_direction = reverse_direction(next_direction)
            
            for dummy_idx in range(6):
                if current_tile[dummy_idx] == color and dummy_idx != current_direction:
                    next_direction = dummy_idx
                    break
            
            next_index = self.get_neighbor(current_index, next_direction)
            current_len += 1
        
        if current_len == len(SOLITAIRE_CODES):
            
            return True
        
        return False

    
# run GUI for Tantrix
import poc_tantrix_gui
print Tantrix(6)
print Tantrix(6).tile_exists((6,0,0))
poc_tantrix_gui.TantrixGUI(Tantrix(6))