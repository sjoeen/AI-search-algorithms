import matplotlib.pyplot as plt
import numpy as np
import random
from rules import rotate_partial,rotate_upward,check

class CubeTower:
    def __init__(self, configuration, parent=None):
        """
        Initializes the cube tower with a given configuration.
        :param configuration: A list of the front-facing colors of the cubes in the tower, starting from the bottom.
        :param parent: The parent node of the current node. (can be used for tracing back the path)
        """
        self.order = ['red', 'blue', 'green','yellow']
        self.configuration = configuration
        self.height = len(configuration)
        self.parent = parent

    def visualize(self):
        """
        Visualizes the current state of the cube tower showing only the front-facing side.
        """
        fig, ax = plt.subplots()
        cube_size = 1  # Size of the cube

        for i, cube in enumerate(self.configuration):
            # Draw only the front-facing side of the cube
            color = cube
            rect = plt.Rectangle((0.5 - cube_size / 2, i), cube_size, cube_size, color=color)
            ax.add_patch(rect)

        ax.set_xlim(0, 1)
        ax.set_ylim(0, self.height)
        ax.set_aspect('equal', adjustable='box')
        ax.axis('off')
        plt.show()

    def visualize_path(self):
        """
        Visualizes the path taken to reach this state from the initial state.
        """
        path = self.get_path()
        fig, ax = plt.subplots()
        cube_size = 1

        for i, configuration in enumerate(path):
            for j, cube in enumerate(configuration):
                color = cube
                rect = plt.Rectangle((i + 0.5 - cube_size / 2, j), cube_size, cube_size, color=color)
                ax.add_patch(rect)

        ax.set_xlim(0, len(path))
        ax.set_ylim(0, self.height)
        ax.set_aspect('equal', adjustable='box')
        ax.axis('off')
        plt.show()

    def get_path(self):
        """
        Retrieves the path taken to reach this state from the initial state.
        """
        path = []
        current = self
        while current.parent is not None:
            path.append(current.configuration)
            current = current.parent
        path.reverse()
        return path
    
    def check_cube(self):
        """
        Check if the cube tower is solved, i.e. all cubes are of the same color.
        """
        return len(set(self.configuration)) == 1

    def rotate_cube(self, index, hold_index=None):
        """
        Rotates a cube and all cubes above it, or up to a held cube.
        :param index: The index of the cube to rotate.
        :param hold_index: The index of the cube to hold, if any.
        """
        # Implement the rotation logic
        pass




def dfs_search(tower,rotations,max_rotations = 10):
    """
    took inspiration from a bruto force sudoku solver algorithm I created last year.
    """
    global global_iteration
        #counts iterations

    if check(tower):
        #Solution is found
        print("\n",tower)
        return True
    
    if rotations == max_rotations:
        #no solutions was found
        return False
    
    for i in range(len(tower)):

        global_iteration += 1
        
        copy_tower = tower.copy()
            #copy tower before modyfiying it, in case of backtracking. 
        rotation = [-1,1]
        for direction in rotation:
            #try both directions
            rotate_upward(tower,i,direction)
            #rotate upwards for given index

            if dfs_search(tower,rotations+1):
                #recurtion
                return True
        
            tower = copy_tower
                #backtrack when reached max depth
    
    return False   


    

def bfs_search(tower,max_iterations = 10000):
    """
    the breadth-first search algoritm, tries all different combinations
    in order to find a solution.

    got a line of code from chatgpt:
    https://chatgpt.com/c/6790a989-d324-800d-8300-e415039f89ce
    """
    
    queue = []
    visited_matrixes = []
        #needs to be a list for flexibility
    visited_matrixes.append(tower.copy())
    queue.append(tower.copy())
        #adds the original state.


    for _ in range(max_iterations):
        current = queue.pop(0)
            #takes out the first element of the queue
        visited_matrixes.append(current)
            #adds the current to visited matrixes

        if check(current):
            print(current)
            print(f"problem solved after {_} iterations using bfs search algorithm.")
            return True
                #solution is found

        for i in range(len(current)):
            rotations = [-1,1]
            for rotation in rotations:
                #loops over all rotations 

                placeholder = current.copy()
                (rotate_upward(placeholder,i,rotation))
                    #finds new matrixes to test

                if not any(np.array_equal(placeholder, arr) for arr in visited_matrixes):
                    #check if a matrix is in visited list
                    queue.append(placeholder)
                        #if not visted, add it to queue 
        
        for idx1 in range(len(current)-1):
            #-1 since start and end cant be the same idx
            for idx2 in range(idx1+1,len(current)):
                #works only with the interval after idx1 is currently at!
                #checks every option in rotate partial function
                rotations = [-1,1]
                for rotation in rotations:
                    #loops over all rotations
                    placeholder = current.copy()
                    rotate_partial(placeholder,idx1,idx2,rotation)

                    if not any(np.array_equal(placeholder, arr) for arr in visited_matrixes):
                        #check if a matrix is in visited list
                        queue.append(placeholder)
                            #if not visted, add it to queue 


    return False
        #no solution was found





def count_rotations(tower):
    """
    use the last row as reference, count amount of rotations required for each row
    to match.
    """

    row,col = tower.shape
    distances = []
    #distances.append(0)
    for i in range(0,row-1):
        for j in range(col):
            #loops over each row and col
            if tower[-1][0] == tower[i][j]:
                distances.append(j)
    return distances

def best_option(tower):
    """
    help function for greedy best algorithm this function decides what
    rotation is the best next move, by looping over each option. 
    """
    best_option = None
    best_start = None
    best_end = None
    best_direction = None
    distances = count_rotations(tower)


    for i in range(0,len(tower)-1):
        #checks all options for rotate upward, 
        #store best result

        rotations = [-1,1]
        for direction in rotations:
            tower_copy = np.copy(tower)
            rotate_upward(tower_copy,i,direction)
            distance_copy = count_rotations(tower_copy)


            if max(distance_copy) <= max(distances):
                if sum(distance_copy) < sum(distances):
                    best_start = i
                    best_option = "upward"
                    best_direction = direction
                    best_end = None

    
        

    for idx1 in range(0,len(tower)-1):
         # -1 since we dont wish to change last idx
        for idx2 in range(idx1+1,len(tower)):
            #works only with the interval after idx1
            #checks every option in rotate partial function

            rotations = [-1,1]
            for direction in rotations:
                tower_copy = np.copy(tower)
                rotate_partial(tower_copy,idx1,idx2,direction)
                distance_copy = count_rotations(tower_copy)

          
                if max(distance_copy) <= max(distances):
                    if sum(distance_copy) < sum(distances):
                        best_start = idx1
                        best_end = idx2
                        best_option = "partial"
                        best_direction = direction


    return best_option,best_start,best_end,best_direction


def greedy_first(tower,max_iter=1000):

    
    for _ in range(max_iter):

        if check(tower):
            #check if we found a solution
            print(tower)
            print(f"problem solved after {_} iterations using greedy first algorithm.")
            return True

        best_options,start,end,direction = best_option(tower)
            #finds optimal next move


        if best_options == "upward":
            rotate_upward(tower,start,direction)
        
        if best_options == "partial":
            rotate_partial(tower,start,end,direction)

    return False

def heuristic(tower):
    """
    Help function for A* algorithm. 
    counts the amount of rows that is identical to the goal 
    (last row), and therefore undershoots how close the algorithm
    is to a solution
    """






# Additional advanced search algorithm
# ...




if __name__ == "__main__":
    initial_configuration = np.array([
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"]  
    ])

    global_iteration = 0
    a = dfs_search(initial_configuration,0)
    print(f"Problem solved after {global_iteration} iterations using dfs algorithm.\n")

    initial_configuration = np.array([
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"]  
    ])
    a = bfs_search(initial_configuration)

    initial_configuration = np.array([
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"]  
    ])
 
    a = greedy_first(initial_configuration)

    tower = np.array([
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"], 
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"], 
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"], 
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"] 
    ])


    a= greedy_first(tower)

    tower = np.array([
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"], 
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"], 
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"], 
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"] 
    ])
    a= bfs_search(tower)

    tower = np.array([
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"], 
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"], 
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"], 
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"],
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"] 
    ])

    a = dfs_search(tower,0)