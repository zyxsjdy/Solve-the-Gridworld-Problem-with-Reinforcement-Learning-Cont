import numpy as np
import copy

def find_element(arr, tar):
    """ 
    function used to find the row and column of an element in the 2d matrix (only for searching unique element)
    Input:
        arr (2d array) - the Gridworld map
        tar (char) - character needed to be found, e.g., 'R'
    Output:
        (i, row.index(tar)) - row and column of the input character on the map
    """
    try:
        for i, row in enumerate(arr):
            if tar in row:
                return (i, row.index(tar)) # return the index of the row (i) and column (row.index(tar))
    except ValueError:
        raise ValueError("Value not found !!!!!!!!!!") # if not found, raise the error
    


#################################################
#### Environment of the gridworld for part 1 ####
#################################################
class Environment_1:

    def __init__(self):
        # set up parameters
        self.n_row = 5
        self.n_col = 5
        self.n_state = self.n_row * self.n_col
        self.n_action = 4

        # Available actions
        #                      left      down      right     up
        self.action =       [ [0, -1],  [1, 0],   [0, 1],   [-1, 0]]
        self.action_text =  ['\u2190', '\u2193', '\u2192', '\u2191']  # unicode text used for visualization

        # Gridworld map
        #             0   1   2   3   4
        self.map = [['T','W','W','W','T'], # 0          map[0][4] = 'T'
                    ['W','W','W','W','W'], # 1
                    ['R','R','W','R','R'], # 2          map[2][3] = 'R'
                    ['W','W','W','W','W'], # 3
                    ['B','W','W','W','W']] # 4          map[4][0] = 'B'

        # Set up the model, (n_state) by (n_action) by (n) by (4) array, for state s and action a,
        # there are n possibilities for transiting to different next state s_, each row is composed of (p, s_, r, t)
        # p  - transition probability from (s,a) to (s_)   ### sum of the n p equals 1
        # s_ - next state
        # r  - reward of the transition from (s,a) to (s_)
        # t  - terminal information, a bool value, True/False

        # Define the initial state "B"
        row_0, col_0 = find_element(self.map, 'B')
        self.state_0 = row_0 * self.n_row + col_0  # calculate the state number based on the place on the map

        self.model = [[[] for _ in range(self.n_action)] for _ in range(self.n_state)]
        for s in range(self.n_state):
            for a in range(self.n_action):
                row, col = np.divmod(s,self.n_row)  # calculate the place on the map based on the state number
                act = self.action[a]  # 0 left, 1 down, 2 right, 3 up
                row_, col_ = row + act[0], col + act[1]  # new positions after action
                state_ = row_ * self.n_row + col_  # calculate the state number based on the place on the map
                outsidecheck = (row_ < 0) or (col_ < 0) or (row_ > self.n_row - 1) or (col_ > self.n_col - 1)  # whether the new position is outside the grid

                # Blue
                if self.map[row][col] == 'B':
                    if outsidecheck:
                        self.model[s][a].append([1.0, s, -1.0, False])  # if want to move out, stay and -1.0
                    else:
                        self.model[s][a].append([1.0, state_, -1.0, False])

                # White
                elif self.map[row][col] == 'W':
                    if outsidecheck:
                        self.model[s][a].append([1.0, s, -1.0, False])  # if want to move out, stay and -1.0
                    elif self.map[row_][col_] == 'R':  # if move to R, jump to start point
                        self.model[s][a].append([1.0, self.state_0, -20.0, False])
                    elif self.map[row_][col_] == 'T':  # if move to terminal state, end
                        self.model[s][a].append([1.0, state_, -1.0, True])
                    else:
                        self.model[s][a].append([1.0, state_, -1.0, False])

                # Red
                elif self.map[row][col] == 'R':  # if current is red, just for indexing
                    self.model[s][a].append([1.0, s, 0.0, False])
                    
                # Black (Terminal)
                elif self.map[row][col] == 'T':  # if current is terminal, just for indexing
                    self.model[s][a].append([1.0, s, 0.0, True])
                
                else:
                    raise ValueError("Unknown value !!!!!!!!!!")
                


#################################################
#### Environment of the gridworld for part 2 ####
#################################################
class Environment_2:

    def __init__(self):
        # set up parameters
        self.n_row = 7
        self.n_col = 7
        self.n_state = self.n_row * self.n_col
        self.n_action = 4

        # Available actions
        #                      left      down      right     up
        self.action =       [ [0, -1],  [1, 0],   [0, 1],   [-1, 0]]
        self.action_text =  ['\u2190', '\u2193', '\u2192', '\u2191']  # unicode text used for visualization

        # Gridworld map
        #             0   1   2   3   4   5   6
        self.map = [['W','W','W','W','W','W','G'], # 0          map[0][6] = 'G'
                    ['W','W','W','W','W','W','W'], # 1
                    ['W','W','W','W','W','W','W'], # 2          map[2][3] = 'W'
                    ['W','W','W','S','W','W','W'], # 3          map[3][3] = 'S'
                    ['W','W','W','W','W','W','W'], # 4
                    ['W','W','W','W','W','W','W'], # 5
                    ['R','W','W','W','W','W','W']] # 6          map[6][0] = 'R'

        # Set up the model, (n_state) by (n_action) by (n) by (4) array, for state s and action a,
        # there are n possibilities for transiting to different next state s_, each row is composed of (p, s_, r, t)
        # p  - transition probability from (s,a) to (s_)   ### sum of the n p equals 1
        # s_ - next state
        # r  - reward of the transition from (s,a) to (s_)
        # t  - terminal information, a bool value, True/False

        # Define the initial state "S"
        row_0, col_0 = find_element(self.map, 'S')
        self.state_0 = row_0 * self.n_row + col_0  # calculate the state number based on the place on the map

        self.model = [[[] for _ in range(self.n_action)] for _ in range(self.n_state)]
        for s in range(self.n_state):
            for a in range(self.n_action):
                row, col = np.divmod(s,self.n_row)  # calculate the place on the map based on the state number
                act = self.action[a]  # 0 left, 1 down, 2 right, 3 up
                row_, col_ = row + act[0], col + act[1]  # new positions after action
                state_ = row_ * self.n_row + col_  # calculate the state number based on the place on the map
                outsidecheck = (row_ < 0) or (col_ < 0) or (row_ > self.n_row - 1) or (col_ > self.n_col - 1)  # whether the new position is outside the grid

                # Start grid
                if self.map[row][col] == 'S':
                    self.model[s][a].append([1.0, state_, 0.0, False])  # normal movement

                # White
                elif self.map[row][col] == 'W':
                    if outsidecheck:
                        self.model[s][a].append([1.0, s, 0.0, False])  # if want to move out, stay
                    elif self.map[row_][col_] == 'R':  
                        self.model[s][a].append([1.0, state_, -1.0, True])  # red terminal
                    elif self.map[row_][col_] == 'G':  
                        self.model[s][a].append([1.0, state_, 1.0, True])  # green terminal
                    else:
                        self.model[s][a].append([1.0, state_, 0.0, False])  # normal movement

                # Red or Green
                elif self.map[row][col] == 'R':  # if current is red, just for indexing
                    self.model[s][a].append([1.0, s, 0.0, True])
                elif self.map[row][col] == 'G':  # if current is green, just for indexing
                    self.model[s][a].append([1.0, s, 0.0, True])

                else:
                    raise ValueError("Unknown value !!!!!!!!!!")
                


                