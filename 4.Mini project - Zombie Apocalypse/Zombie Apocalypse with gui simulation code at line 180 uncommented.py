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
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
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
        self._zombie_list.append((row, col))
                
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
        self._human_list.append((row, col))
        
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
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        #print self
        #print self.is_empty(1,1)
        #width = self.get_grid_width()
        #height = self.get_grid_height()
        visited = poc_grid.Grid(self.get_grid_height(), self.get_grid_width())
        distance_field = [[self.get_grid_width()*self.get_grid_height() for dummy_col in range(self.get_grid_width())] for dummy_row in range(self.get_grid_height())]
        
        boundary = poc_queue.Queue()
        if entity_type.lower() == 'human':
            for human in self.humans():
                boundary.enqueue(human)
                visited.set_full(human[0], human[1])
                distance_field[human[0]][human[1]] = 0
        elif entity_type.lower() == 'zombie':
            for zombie in self.zombies():
                boundary.enqueue(zombie)
                visited.set_full(zombie[0], zombie[1])
                distance_field[zombie[0]][zombie[1]] = 0
        
        while (len(boundary) != 0): 
            current_cell = boundary.dequeue()
            neighbors = self.four_neighbors(current_cell[0], current_cell[1])
            for neighbor in neighbors:
                #first check if this particular neighbor cell is an obstacle
                if self.is_empty(neighbor[0], neighbor[1]):
                    if visited.is_empty(neighbor[0], neighbor[1]):
                        visited.set_full(neighbor[0], neighbor[1])
                        boundary.enqueue(neighbor)        
                        neighbor_distance = distance_field[neighbor[0]][neighbor[1]]
                        current_cell_distance = (distance_field[current_cell[0]][current_cell[1]]) + 1
                        distance_field[neighbor[0]][neighbor[1]] = min(neighbor_distance, current_cell_distance)
        return distance_field
        
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        width = self.get_grid_width()
        height = self.get_grid_height()
        visited = poc_grid.Grid(height, width)
        obstacle = len(zombie_distance) * len(zombie_distance[0])
        #print obstacle
        
        human_list = []
        for human in self.humans():
            neighbors = visited.eight_neighbors(human[0], human[1])
            best_moves = {}
            best_moves[zombie_distance[human[0]][human[1]]] = human
            for neighbor in neighbors:
                if zombie_distance[neighbor[0]][neighbor[1]] != obstacle:
                    if zombie_distance[neighbor[0]][neighbor[1]] > zombie_distance[human[0]][human[1]]:
                        best_moves[zombie_distance[neighbor[0]][neighbor[1]]] = neighbor
            human_list.append(best_moves[max(best_moves)])
        self._human_list = human_list
        #print self._human_list
        
        
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        width = self.get_grid_width()
        height = self.get_grid_height()
        visited = poc_grid.Grid(height, width)
        
        zombie_list = []
        for zombie in self.zombies():
            neighbors = visited.four_neighbors(zombie[0], zombie[1])
            best_moves = {}
            best_moves[human_distance[zombie[0]][zombie[1]]] = zombie
            for neighbor in neighbors:
                if human_distance[neighbor[0]][neighbor[1]] < human_distance[zombie[0]][zombie[1]]:
                    best_moves[human_distance[neighbor[0]][neighbor[1]]] = neighbor
            zombie_list.append(best_moves[min(best_moves)])
        self._zombie_list = zombie_list
        #print self._zombie_list

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Zombie(30, 40))

#my test
#obj = Zombie(3, 3, [], [], [(2, 2)])
#print obj.compute_distance_field('human')
#expected
#[[4, 3, 2], [3, 2, 1], [2, 1, 0]]


#obj = Zombie(4, 6, [], [(1, 5), (3, 2)], [])
#print obj.compute_distance_field('zombie') 
##expected 
##[[5, 4, 3, 3, 2, 1], [4, 3, 2, 2, 1, 0], [3, 2, 1, 2, 2, 1], [2, 1, 0, 1, 2, 2]] 


#obj = Zombie(3, 3, [(0, 1), (1, 1)], [(0, 0)], [(2, 0)])
##print obj
#print obj.compute_distance_field('zombie')


#obj = Zombie(3, 3, [], [(2, 2)], [(1, 1)])
#dist = [[4, 3, 2], [3, 2, 1], [2, 1, 0]]
#print obj.move_humans(dist)
#then obj.humans() expected location to be one of [(0, 0)] but
#received (1, 1)


#obj = Zombie(3, 3, [], [(1, 1)], [(2, 2)])
#dist = [[4, 3, 2], [3, 2, 1], [2, 1, 0]]
#print obj.move_zombies(dist) 
#then obj.zombies() expected location to be one of [(1, 2), (2, 1)]
#but received (1, 1)

