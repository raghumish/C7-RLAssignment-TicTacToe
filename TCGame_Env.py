from gym import spaces
import numpy as np
import random
from itertools import groupby
from itertools import product



class TicTacToe():

    def __init__(self):
        """initialise the board"""
        
        # initialise state as an array
        self.state = [np.nan for _ in range(9)]  # initialises the board position, can initialise to an array or matrix
        # all possible numbers
        self.all_possible_numbers = [i for i in range(1, len(self.state) + 1)] # , can initialise to an array or matrix

        self.reset()


    def is_winning(self, curr_state):
        """Takes state as an input and returns whether any row, column or diagonal has winning sum
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan]
        Output = False"""
        
        win_positions = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        #print("is winning curr state = ", curr_state)
        
        for pattern in win_positions:
            if (np.isnan(curr_state[pattern[0]]) or np.isnan(curr_state[pattern[1]]) or np.isnan(curr_state[pattern[2]])):
                #print('first row state = ', curr_state[pattern[0]], curr_state[pattern[1]], curr_state[pattern[2]])
                return False
            else:
                sum_pattern = (curr_state[pattern[0]] + curr_state[pattern[1]] + curr_state[pattern[2]])
                #print('sum of first row = ', sum_pattern)
                if sum_pattern != 15:
                    return False
                else:
                    return True
 

    def is_terminal(self, curr_state):
        # Terminal state could be winning state or when the board is filled up
        #print('is terminal curr state = ', curr_state)
        if self.is_winning(curr_state) == True:
            return True, 'Win'

        elif len(self.allowed_positions(curr_state)) == 0:
            return True, 'Tie'

        else:
            return False, 'Resume'


    def allowed_positions(self, curr_state):
        """Takes state as an input and returns all indexes that are blank"""
        return [i for i, val in enumerate(curr_state) if np.isnan(val)]


    def allowed_values(self, curr_state):
        """Takes the current state as input and returns all possible (unused) values that can be placed on the board"""

        used_values = [val for val in curr_state if not np.isnan(val)]
        agent_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 !=0]
        env_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 ==0]

        return (agent_values, env_values)


    def action_space(self, curr_state):
        """Takes the current state as input and returns all possible actions, i.e, all combinations of allowed positions and allowed values"""

        agent_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[0])
        env_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[1])
        return (agent_actions, env_actions)



    def state_transition(self, curr_state, curr_action):
        """Takes current state and action and returns the board position just after agent's move.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = [1, 2, 3, 4, nan, nan, nan, 9, nan]
        """
        curr_state[curr_action[0]] = curr_action[1]
        return curr_state
        
      

    def step(self, curr_state, curr_action):
        """Takes current state and action and returns the next state, reward and whether the state is terminal. Hint: First, check the board position after
        agent's move, whether the game is won/loss/tied. Then incorporate environment's move and again check the board status.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = ([1, 2, 3, 4, nan, nan, nan, 9, nan], -1, False)"""

        stop_play = []
        #print('curr state at step curr state = ', curr_state)
        agent_play = self.state_transition(curr_state, curr_action)
        #print('agent play at step agent play = ', agent_play)
        #print('curr action at step curr action = ', curr_action)
        stop_play, result = self.is_terminal(agent_play)
        if stop_play == True:
            if result == 'Win':
                reward = 10
            else:
                reward = 0
        else:
            #print('agent play at step else loop = ', agent_play)
            env_position = random.choice(self.allowed_positions(agent_play))     # using agent_play to check allowed positions
            #print('env position = ', env_position)
            agent_values, env_values = (self.allowed_values(agent_play))         # random choice of play by env
            #print('env allowed values = ', env_values)
            env_val = random.choice(env_values)
            #print('env chosen value = ', env_val)
            agent_play[env_position] = env_val                                   # This is the current state of play
            stop_play, result = self.is_terminal(agent_play)
            if stop_play == True:
                if result == 'Win':
                    reward = -10
                else:
                    reward = 0
            else:
                reward = -1
        return agent_play, reward, stop_play
        

    def reset(self):
        return self.state
