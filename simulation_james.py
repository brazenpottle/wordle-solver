import entropy 
import os 
import pandas as pd
import time 
import json
from multiprocessing import Pool
import numpy as np
possible_answers_path = os.path.join('data', 'possible_answers.txt')
possible_answers = list(pd.read_csv(possible_answers_path, header=None)[0])
possible_answers_split = entropy.split_word_list(possible_answers)
def determine_correctness_array(target_word,curr_word):
    correctness_array = [None]*len(target_word)
    for index_1, letter_1 in enumerate(curr_word):
        if letter_1 not in target_word:
            correctness_array[index_1] = 0
        elif letter_1 in target_word and letter_1 == target_word[index_1]:
            correctness_array[index_1] = 2
        else:
            correctness_array[index_1] = 1
    return correctness_array

def simulate(target_word, best_word, word_list_split, fn):
    no_tries = 1
    while best_word != target_word:
        correctness_array = determine_correctness_array(target_word, best_word)
        best_word, word_list_split = entropy.pick_word(best_word, word_list_split, correctness_array, fn)
        no_tries += 1
    return (no_tries, best_word)

def expected_value(p, x):
    e = 0
    for i, j in enumerate(p):
        e += x[i]*j
    return e

def simulation(start_word, word_list, allowable_word_list, fn):
    word_list_split = entropy.split_word_list(allowable_word_list)
    word_no_tries = {}
    total_counts = {}
    for word in word_list:
        no_tries, word = simulate(word, start_word, word_list_split, fn)
        total_counts[no_tries] = total_counts.get(no_tries, 0) + 1
        word_no_tries[no_tries] = word_no_tries.get(no_tries, []) + [word]
    json.dump(total_counts, open('simulation_counts.json', 'w'))
    json.dump(word_no_tries, open('simulation_word_counts.json','w'))
    
def simulation_multiprocessing(target_word):
    no_tries = 1
    best_word = 'tares'
    word_list_split = entropy.allowable_guesses_split
    fn = entropy.entropy 
    while best_word != target_word:
        correctness_array = determine_correctness_array(target_word, best_word)
        best_word, word_list_split = entropy.pick_word(best_word, word_list_split, correctness_array, fn)
        no_tries += 1
    return (no_tries, best_word)
    
if __name__ == '__main__':
    start = time.time()
    with Pool(os.cpu_count()-1) as p:
        data = p.map(simulation_multiprocessing, possible_answers)
    np.savetxt("simulation_entropy_1.csv", data, delimiter = ',', fmt = '% s')
    end = time.time()
    print(end-start)
    #print(simulate('frogs', 'tares', entropy.allowable_guesses_split ,entropy.entropy))