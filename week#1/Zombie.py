"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row,col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row,col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human in self._human_list:
            yield human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        visited = poc_grid.Grid(self._grid_height, self._grid_width)
        
        distance_field = [[self._grid_height * self._grid_width for dummy_col in range(self._grid_width)] 
                       for dummy_row in range(self._grid_height)]
        
        
        boundary = poc_queue.Queue()
        
        if entity_type == ZOMBIE:
            type_list = self._zombie_list
        elif entity_type == HUMAN:
            type_list = self._human_list
        
        
        for item in type_list:
            
            visited.set_full(item[0], item[1])
            distance_field[item[0]][item[1]] = 0
            boundary.enqueue(item)
        
        while len(boundary) > 0:
            
            current_cell = boundary.dequeue()
            
            all_neigh = visited.four_neighbors(current_cell[0], current_cell[1])
            
            for neigh_cell in all_neigh:
                if visited.is_empty(neigh_cell[0],neigh_cell[1]) and self.is_empty(neigh_cell[0],neigh_cell[1]):
                    
                    visited.set_full(neigh_cell[0],neigh_cell[1])
                    
                    boundary.enqueue(neigh_cell)
                    
                    distance_field[neigh_cell[0]][neigh_cell[1]] = distance_field[current_cell[0]][current_cell[1]]+ 1
        
        #min(distance_field[neigh_cell[0]][neigh_cell[1]],distance_field[current_cell[0]][current_cell[1]]+ 1)
        
        
        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        dummy_humans = []
        #print self._human_list
        for human in self._human_list:
            neighbors = self.eight_neighbors(human[0], human[1])
            
            new_row = human[0]
            new_col = human[1]
            new_dist = zombie_distance_field[new_row][new_col]
            #print new_dist
            for neigh in neighbors:
                if zombie_distance_field[neigh[0]][neigh[1]] >= new_dist and self.is_empty(neigh[0],neigh[1]):
                    new_row = neigh[0]
                    new_col = neigh[1]
                    new_dist = zombie_distance_field[neigh[0]][neigh[1]]
            
            dummy_humans.append((new_row, new_col))
        
        self._human_list = dummy_humans
        
         
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        dummy_zombies = []
        
        for zombie in self._zombie_list:
            neighbors = self.four_neighbors(zombie[0], zombie[1])
            
            new_row = zombie[0]
            new_col = zombie[1]
            new_dist = human_distance_field[new_row][new_col]
            
            for neigh in neighbors:
                if human_distance_field[neigh[0]][neigh[1]] <= new_dist and self.is_empty(neigh[0],neigh[1]):
                    new_row = neigh[0]
                    new_col = neigh[1]
                    new_dist = human_distance_field[neigh[0]][neigh[1]]
            
            dummy_zombies.append((new_row, new_col))
        
        self._zombie_list = dummy_zombies

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(30, 40))
