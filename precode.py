import matplotlib.pyplot as plt
import numpy as np
from rules import rotate_partial,rotate_upward,check
import tracemalloc
import time

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
        first_row = CubeTower(list(tower[:, 0]))
        first_row.visualize()
        print(f"problem solved after {global_iteration} iterations using dfs search algorithm.")
        return True,global_iteration
    
    if rotations == max_rotations:
        #no solutions was found
        return False,global_iteration
    
    for i in range(len(tower)):

        global_iteration += 1
        
        copy_tower = tower.copy()
            #copy tower before modyfiying it, in case of backtracking. 
        rotation = [-1,1]
        for direction in rotation:
            #try both directions
            rotate_upward(tower,i,direction)
            #rotate upwards for given index

            result, iteration_count = dfs_search(tower, rotations + 1, max_rotations)
            if result:
                return True, iteration_count
        
            tower = copy_tower
                #backtrack when reached max depth
    
    return False,global_iteration


    

def bfs_search(tower, max_iterations=10000):
    """
    The breadth-first search algorithm, tries all different combinations
    in order to find a solution.
    """
    queue = []
    visited_matrixes = set() 
    initial_state = tuple(map(tuple, tower))  
    visited_matrixes.add(initial_state)
    queue.append(tower.copy())  
        # Adds the original state.

    for _ in range(max_iterations):
        if not queue:
            return False  
                # No solution was found

        current = queue.pop(0)  
            # Takes out the first element of the queue

        if check(current):
            # Solution is found
            first_row = CubeTower(list(current[:, 0]))
            first_row.visualize()
            print(f"Problem solved after {_} iterations using BFS search algorithm.")
            return True,_

        # Generate new states using rotate_upward
        for i in range(len(current)):
            rotations = [-1, 1]
            for rotation in rotations:
                # Loops over all rotations
                placeholder = current.copy()
                rotate_upward(placeholder, i, rotation)  
                    # Rotate upwards for given index

                # Check if the new state has been visited
                state_tuple = tuple(map(tuple, placeholder))  
                if state_tuple not in visited_matrixes:
                    visited_matrixes.add(state_tuple)
                    queue.append(placeholder) 
                         # If not visited, add it to the queue

        # Generate new states using rotate_partial
        for idx1 in range(len(current) - 1):
            # -1 since start and end can't be the same index
            for idx2 in range(idx1 + 1, len(current)):
                # Works only with the interval after idx1 is currently at!
                # Checks every option in rotate_partial function
                rotations = [-1, 1]
                for rotation in rotations:
                    # Loops over all rotations
                    placeholder = current.copy()
                    rotate_partial(placeholder, idx1, idx2, rotation)

                    # Check if the new state has been visited
                    state_tuple = tuple(map(tuple, placeholder)) 
                    if state_tuple not in visited_matrixes:
                        visited_matrixes.add(state_tuple)
                        queue.append(placeholder)  
                            # If not visited, add it to the queue

    return False,max_iterations
        # No solution was found 


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


def greedy_best_first(tower,max_iter=1000):

    rotation_count = 0
    
    for _ in range(max_iter):

        if check(tower):
            #check if we found a solution
            print(f"problem solved after {_} iterations using greedy best-first algorithm.")
            print(f"Number of rotations: {rotation_count}")
            first_row = CubeTower(list(tower[:, 0]))
            first_row.visualize()

            return True,rotation_count

        best_options,start,end,direction = best_option(tower)
            #finds optimal next move


        if best_options == "upward":
            rotate_upward(tower,start,direction)
            rotation_count +=1
        
        if best_options == "partial":
            rotate_partial(tower,start,end,direction)
            rotation_count +=1

    return False,max_iter

def heuristic(tower):
    """
    heuristic help function for A* algorithm. 
    """
    rotations = count_rotations(tower) # heuristics is calculated as the sum of the rotations
    return sum(rotations)

def get_neighbours(tower): # Function to get all the neighbours of a given node
    get_neighbours = []
    rows = tower.shape[0]
    for i in range(rows):
        for direction in [-1, 1]:
            neighbour = np.copy(tower)
            rotate_upward(neighbour, i, direction)
            get_neighbours.append(neighbour)
    for start in range(rows):
        for end in range(start + 1, rows + 1):
            for direction in [-1, 1]:
                neighbour = np.copy(tower)
                rotate_partial(neighbour, start, end, direction)
                get_neighbours.append(neighbour)
    return get_neighbours # Returns a list of all the neighbouring nodes

def a_star_search(tower, max_iter=1000):
    open_list = [(tower, heuristic(tower))] # List to keep track of the nodes to be evaluated. Tower is initialized as the starting node
    g_score = {tuple(tower.flatten()): 0} # A dictionary of the g score of each node
    f_score = {tuple(tower.flatten()): heuristic(tower)} # A dictionary of the f score of each node
    closed_list = set() # A set to keep track of the nodes that have been evaluated.
    for _ in range(max_iter):
        if not open_list:
            return False
        
        open_list.sort(key=lambda x: x[1]) # Sort the open list by the f score
        current, current_fscore = open_list.pop(0) # Get the node with the lowest f score and expand from it
        
        closed_list.add(tuple(current.flatten())) # Add the current node to the closed list

        if check(current):
            tower[:] = current
            print(f"Problem solved after {_} iterations using A* algorithm.")
            print(f"Number of rotations: {g_score[tuple(current.flatten())]}")
            print(f"Number of unique nodes: {len(set(g_score.keys()))}")
            first_row = CubeTower(list(tower[:, 0]))
            first_row.visualize()


            return True,g_score[tuple(current.flatten())] 
                # Return True and rotations if solved
        
        for neighbour in get_neighbours(current): # Get the neighbours of the current node

            if tuple(neighbour.flatten()) in closed_list:
                continue # Skip the neighbour if it is in the closed list

            tentative_g_score = g_score[tuple(current.flatten())] + 1 # Calculate the tentative g score, which is the g score of the current node + 1 (since the cost of moving to a neighbour is 1)
            if tentative_g_score < g_score.get(tuple(neighbour.flatten()), float('inf')): # Check if the tentative g score is less than the g score of the neighbour (or infinity if the neighbour has not been discovered yet)
                g_score[tuple(neighbour.flatten())] = tentative_g_score # Update the g score of the neighbour
                f_score[tuple(neighbour.flatten())] = g_score[tuple(neighbour.flatten())] + heuristic(neighbour) # Update the f score of the neighbour
                open_list.append((neighbour, f_score[tuple(neighbour.flatten())])) # Add the neighbour to the open list

    return False,max_iter




def test(algorithm, max_iterations=1000):
    """
    test function that plots memory used, time and amount of rotations.
    """

    towers = [
        np.array([  # 3 cubes
            ["red", "blue", "green", "yellow"],  
            ["blue", "green", "yellow", "red"], 
            ["green", "yellow", "red", "blue"]  
        ]),
        np.array([  # 4 cubes
            ["red", "blue", "green", "yellow"],  
            ["blue", "green", "yellow", "red"], 
            ["green", "yellow", "red", "blue"],  
            ["yellow", "red", "blue", "green"]
        ]),
        np.array([  # 6 cubes
            ["red", "blue", "green", "yellow"],  
            ["blue", "green", "yellow", "red"], 
            ["green", "yellow", "red", "blue"],  
            ["yellow", "red", "blue", "green"],
            ["red", "blue", "green", "yellow"],  
            ["blue", "green", "yellow", "red"]
        ]),
        np.array([  # 10 cubes
            ["red", "blue", "green", "yellow"],  
            ["blue", "green", "yellow", "red"], 
            ["green", "yellow", "red", "blue"],  
            ["yellow", "red", "blue", "green"],
            ["red", "blue", "green", "yellow"],  
            ["blue", "green", "yellow", "red"], 
            ["green", "yellow", "red", "blue"],  
            ["yellow", "red", "blue", "green"],
            ["red", "blue", "green", "yellow"],  
            ["blue", "green", "yellow", "red"]
        ]),
        np.array([  # 15 cubes
            ["red", "blue", "green", "yellow"],  
            ["blue", "green", "yellow", "red"], 
            ["green", "yellow", "red", "blue"],  
            ["yellow", "red", "blue", "green"],
            ["red", "blue", "green", "yellow"],  
            ["blue", "green", "yellow", "red"], 
            ["green", "yellow", "red", "blue"],  
            ["yellow", "red", "blue", "green"],
            ["red", "blue", "green", "yellow"],  
            ["blue", "green", "yellow", "red"], 
            ["green", "yellow", "red", "blue"],  
            ["yellow", "red", "blue", "green"],
            ["red", "blue", "green", "yellow"],  
            ["blue", "green", "yellow", "red"], 
            ["green", "yellow", "red", "blue"]
        ])
    ]


    tower_sizes = [3, 4, 6, 10, 15]
    times = []
    memories = []
    rotations = []
    solved = []
        #all data needed


    for i, tower in enumerate(towers):

        front_colors = list(tower[:, 0])
        cubetower = CubeTower(front_colors)
        cubetower.visualize()
            #visualize start state for each cube

        
        start_time = time.time()
        tracemalloc.start()
            #time and memory tracking

    
        result,rotation_count = algorithm(tower, max_iterations)
            #run algorithm
        

        elapsed_time = time.time() - start_time
        current_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()
            #track memory and time usage


        
        times.append(elapsed_time)
        memories.append(peak_mem/ 1024**2)
            #convert from bytes to MB
        rotations.append(rotation_count)
        solved.append(result is not False)
            #save results

        
        print(f"Time: {elapsed_time:.4f} seconds")
        print(f"Max memory: {round(peak_mem / 1024**2,3)} MB")
            #convert from bytes to MB
        print(f"Amount of rotations: {rotation_count}")
        print(f"Solution: {result}")
            #results


    plt.figure(figsize=(15, 5))


    plt.subplot(1, 3, 1)
    plt.plot(tower_sizes, times, marker='o')
    plt.title("Time compared to cubesize")
    plt.xlabel("Amount of cubes")
    plt.ylabel("Time (seconds)")

    
    plt.subplot(1, 3, 2)
    plt.plot(tower_sizes, memories, marker='o', color='orange')
    plt.title("Memory compared to cubesize")
    plt.xlabel("Amount of cubes")
    plt.ylabel("Memory (MB)")

    
    plt.subplot(1, 3, 3)
    plt.plot(tower_sizes, rotations, marker='o', color='green')
    plt.title("Rotations compared to cubesize")
    plt.xlabel("Amount of cubes")
    plt.ylabel("Amount of rotations")

    plt.tight_layout()
    plt.show()



    if all(solved):
        print("Algoritmen solved all cubes.")
    else:
        print("Algoritmen could not solve all cubes.")



if __name__ == "__main__":


    global_iteration = 0
    print("DFS:\n")
    test(dfs_search,0)
    print("\n\n\ngreedy best first:\n\n")
    test(greedy_best_first)
    print("\n\n\nA*:\n\n")
    test(a_star_search)
    print("\n\n\nBFS:\n\n")
    test(bfs_search,10000)
