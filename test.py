import numpy as np
from rules import rotate_upward,rotate_partial,check

def count_rotations(tower):
    """
    use the last row as reference, count amount of rotations required for each row
    to match by counting idx distance since the cube only rotates one way store in a
    list and return
    """

    row,col = tower.shape
    distances = []
    #distances.append(0)
    for i in range(0,row-1):
        for j in range(col):
            if tower[-1][0] == tower[i][j]:
                distances.append(j)
    return distances

def best_option(tower):
    """
    help function for A* algorithm
    this function decides what rotation option is best to solve the algorithm. 
    """
    best_option = None
    best_start = None
    best_end = None
    best_direction = None
    distances = count_rotations(tower)



    for i in range(0,len(tower)):

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

        #if sum(count_rotations(tower_copy)) == 0:
            #return best_option,best_start,best_end
    
        

    for idx1 in range(0,len(tower)-1):
         #-1 since start and end cant be the same idx
        for idx2 in range(idx1+1,len(tower)):
            #works only with the interval after idx1 is currently at!
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

            #if sum(count_rotations(distance_copy)) == 0:
                #return best_option,best_start,best_end

    return best_option,best_start,best_end,best_direction


def greedy_first(tower,max_iter=1000):


    
    for _ in range(max_iter):

        if check(tower):
            #check if we found a solution
            #print(tower)
            print(_)
            return True

        best_options,start,end,direction = best_option(tower)
            #finds optimal next move


        if best_options == "upward":
            rotate_upward(tower,start,direction)
        
        if best_options == "partial":
            rotate_partial(tower,start,end,direction)

    return False

if __name__ == "__main__":
    initial_configuration = np.array([
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"]  
    ])
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

    print(count_rotations(initial_configuration))
    greedy_first(tower)
    print(tower)