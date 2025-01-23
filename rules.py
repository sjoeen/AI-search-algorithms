import numpy as np

def rotate_upward(tower,index,rotation):
    """
    Rotate all the cubes on a given index and upward 90 degrees to the right

    parameters: tower (np.array),index

    https://numpy.org/doc/2.1/reference/generated/numpy.roll.html
    """

    rotate_rows = tower[0:index+1:]
        #slice all rows from start to given index
    rotated_rows = np.roll(rotate_rows,shift=rotation,axis=1)
        #rotate desired rows
    tower[0:index+1] = rotated_rows
        #slice rows back into original data

def check(tower):
    """
    checks if all rows are identical with the first one. 
    https://numpy.org/doc/2.1/reference/generated/numpy.all.html
    """

    return np.all(tower == tower[0])


def rotate_partial(tower,start,end,rotation):
    """
    rorate all the cubes from within an interval where the last index is not included ( [ > )
    parameters: tower (np array),index
    """

    rotate_rows = tower[start:end]
        #slice
    rotated_rows = np.roll(rotate_rows,shift=rotation,axis=1)
        #rotate desired rows
    tower[start:end] = rotated_rows
        #slice them back into original data


if __name__ == "__main__":

    tower = np.array([
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"]  
    ])
    print("før:\n", tower)

    rotate_upward(tower,1)
    print("etter upward:\n", tower)

    tower = np.array([
        ["red", "blue", "green", "yellow"],  
        ["blue", "green", "yellow", "red"], 
        ["green", "yellow", "red", "blue"]  
    ])
    rotate_partial(tower,2,3)
    print("etter partial:\n",tower )
