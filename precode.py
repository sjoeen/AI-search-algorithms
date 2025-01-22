import matplotlib.pyplot as plt
import numpy as np
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
    took inspiration from a bruto force sudoku solver algorithm i created last year,
    and modified it simpler.
    My code was inspired again by this code:
    https://gist.github.com/syphh/62e6140361feb2d7196f2cb050c987b3
    """
    global global_iteration
        #counts iterations

    if check(tower):
        print("\n",tower)
        return True
    
    if rotations == max_rotations:
        #no solutions was found
        return False
    
    for i in range(len(tower)):

        global_iteration += 1
        print(f"\n",tower)
            #test statements, remove afterwards
        
        copy_tower = tower.copy()
            #copy tower before modyfiying it, in case of backtracking. 

        rotate_upward(tower,i)
            #rotate upwards for given index

        if dfs_search(tower,rotations+1):
            #breaks loop if the nextt rotation solves the problem. 
            return True
        
        tower = copy_tower
            #backtrack when reached max depth
    
    return False   


    

def bfs_search(tower):
    # Implement Breadth-First Search
    pass

def a_star_search(tower):
    # Implement A* Search
    pass

# Additional advanced search algorithm
# ...



if __name__ == "__main__":
    initial_configuration = np.array([
        ["red", "blue", "green", "yellow"],  # Nederste kube
        ["blue", "green", "yellow", "red"], # Midterste kube
        ["green", "yellow", "red", "blue"]  # Øverste kube
    ])

    global_iteration = 0
    a = dfs_search(initial_configuration,0)
    print(f"\nProblem solved after {global_iteration} iterations using dfs algorithm.")