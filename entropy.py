import numpy as np 
import os
import pandas as pd
import time 
import itertools 
from multiprocessing import Pool
from preprocessing import allowable_guesses, possible_answers
# from numba import jit

# read in data
# allowable_guesses = np.array(pd.read_csv("data/allowable_guesses.txt", header=None)[0])

def split_word_list(the_list):
    split_list = []
    for i in range(len(the_list)):
        split_list.append(list(the_list[i]))
    return np.array(split_list)

allowable_guesses_split = split_word_list(allowable_guesses)
'''
def generate_permutations(word): # for 
    permutations = []
    word_split = list(word)
    index = -1
    length = len(word_split)
    word_indexing = []

    for i in range(length):
        curr_letter = word_split[i]
        if curr_letter not in word_split[:i]:
            index +=1
            word_indexing.append(index)
        else:
            word_indexing.append(word_split.index(curr_letter))
    indexed_permutations = list(itertools.product(range(3), repeat = index +1))
    for permutation in indexed_permutations:
        index_permutation = [None]*(len(word_split))
        for a, b in enumerate(permutation):
            for i, j in enumerate(word_indexing):
                if a == j:
                    index_permutation[i] = b
        permutations.append(index_permutation)
    return permutations
'''

def generate_permutations(word): 
    final_permutations = []
    permutations = []

    word_split = list(word)
    counter = -1
    
    length = len(word_split)
    
    word_indexing = []

    for idx, letter in enumerate(word_split):
        if letter not in word_split[:idx]:
            counter +=1
            word_indexing.append(counter)
        else:
            word_indexing.append(word_split.index(letter))
    dupe_dict = {}
    for i, j in enumerate(word_indexing):
        dupe_dict[j] = dupe_dict.get(j,[] ) + [i]
    dupe_dict_2 = {}
    for key, value in dupe_dict.items():
        if len(value) > 1:
            dupe_dict_2[key] = value
    dupe_1 = [0]
    dupe_2 = [1,2]
    no_dupe_0 = [0,1,2]
    is_dupe = [1,2] # choice to use either dupe_1 or dupe_2
    no_of_dupes = len(dupe_dict_2)
    variations = []       
    if no_of_dupes > 0:
        dupe_permutations = itertools.product(is_dupe, repeat = no_of_dupes)
        for permutation in dupe_permutations:
            counter = 0
            variation = [0]*len(word)
            for key, values in dupe_dict_2.items():
                for index in values:
                    variation[index] = permutation[counter]
                counter += 1        
            variations.append(variation)
    else:
        variations.append([0]*len(word))
    for variation in variations:
        for index, choice in enumerate(variation):
            if choice == 0:
                variation[index] = no_dupe_0
            elif choice == 1:
                variation[index] = dupe_1
            else:
                variation[index] = dupe_2
        permutations.append(variation)
    for permutation in permutations:
        final_permutations.extend(list(itertools.product(*permutation)))
    return final_permutations


def possible_words_2(array, word, word_list_split): #returns possible words split; much faster
    for index, correct_letter in enumerate(array):
        if correct_letter == 2:
            word_list_split = word_list_split[word_list_split[:, index] == word[index]]
        elif correct_letter ==1:
            word_list_split = word_list_split[word_list_split[:, index] != word[index]]
            word_list_split = word_list_split[np.any(word_list_split == word[index], axis =1)]
        else:
            word_list_split = word_list_split[np.sum(word_list_split == word[index],axis = 1) == 0]
    return word_list_split

def possible_words_length_2(array, word, word_list_split): #returns possible words split; much faster
    for index, correct_letter in enumerate(array):
        if correct_letter == 2:
            word_list_split = word_list_split[word_list_split[:, index] == word[index]]
        elif correct_letter ==1:
            word_list_split = word_list_split[word_list_split[:, index] != word[index]]
            word_list_split = word_list_split[np.any(word_list_split == word[index], axis =1)]
        else:
            word_list_split = word_list_split[np.sum(word_list_split == word[index],axis = 1) == 0]
    return len(word_list_split)

def entropy_2(word, word_list_split): #use this
    total_number = len(allowable_guesses)
    expected_value = 0
    permutations = generate_permutations(word)
    for permutation in permutations:
        no_words = possible_words_length_2(permutation, word, word_list_split)
        p = no_words/total_number
        if p != 0:
            expected_value += p*np.log2(1/p)
    return expected_value

def entropy_2_1(p):
    return entropy_2(p, allowable_guesses_split)
   
def pick_word(word, word_list_split, correctness_array, fn):
    word_list_split = possible_words_2(correctness_array, word, word_list_split)
    def mapping(wd):
        return fn(wd,word_list_split)
    if len(word_list_split) != 0:
        max_ind = np.argmax(np.apply_along_axis(mapping, arr = word_list_split, axis = 1))
        return (''.join(word_list_split[max_ind]), word_list_split)
    else:
        return []
    '''
    x = np.array(allowable_guesses_split)
    y = np.array(allowable_guesses)
    def entropy_2_1(p):
        return entropy_2(p, x)
    start = time.time()
    with Pool(os.cpu_count()-1) as p:
        data = p.map(entropy_2_1, y)
    np.savetxt("entropies.csv", data, delimiter = ',', fmt = '% s')
    end = time.time()
    print(end-start)
'''
if __name__ == "__main__":
    x = allowable_guesses_split
    word = input('Enter the five letter word you put: ') 
    correctness_array = list(map(int,list(input('Enter the correctness array: '))))
    x = possible_words_2(correctness_array, word, x)
    new_list = []
    for wd in x:
        new_list.append((wd,entropy_2(wd,x)))
    df = pd.DataFrame(new_list).sort_values(1, ascending = True)
    print(df)
    while 1:
        word = input('Enter the five letter word you put: ') 
        correctness_array = list(map(int,list(input('Enter the correctness array: '))))
        x = possible_words_2(correctness_array, word, x)
        new_list = []
        for wd in x:
            new_list.append((wd,entropy_2(wd,x)))
        df = pd.DataFrame(new_list).sort_values(1, ascending = True)
        print(df)

'''
x = np.array(allowable_guesses_split)
start = time.time()
print(entropy_2('slate',x))
end = time.time()
print(end-start)
start = time.time()
print(entropy('tares',allowable_guesses))
end = time.time()
print(end-start)
'''
'''
    def pick_word_mp(perm):
        return pick_word('tares',allowable_guesses_split, perm, entropy_2)
    def precomputer(word,word_list_split,fn):
        permutations = generate_permutations(word)
        with Pool(os.cpu_count()) as p:
            data = p.map(pick_word_mp, permutations)
        return data
    start = time.time()
    print(precomputer('tares',allowable_guesses_split, entropy_2))
    end = time.time()
    print(end-start)
'''