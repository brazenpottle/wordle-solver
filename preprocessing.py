# preprocessing to save computation time
import numpy as np

allowable_guesses = []
with open("data/allowable_guesses.txt", 'r') as g:    
    for line in g:
        allowable_guesses.append(line.strip('\n'))
allowable_guesses = np.array(allowable_guesses)

possible_answers = []
with open("data/possible_answers.txt") as f:
    for line in f:
        possible_answers.append(line.strip('\n'))
possible_answers = np.array(possible_answers)