import numpy as np 
import os
import pandas as pd
import time 
import itertools 
from multiprocessing import Pool

allowable_guesses_path = os.path.join('data', 'allowable_guesses.txt')
allowable_guesses = list(pd.read_csv(allowable_guesses_path, header=None)[0])

def split_word_list(the_list):
    split_list = []
    for i in range(len(the_list)):
        split_list.append(list(the_list[i]))
    return split_list

allowable_guesses_split = split_word_list(allowable_guesses)

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

def possible_words_number_s(array, word,word_list_split):
    total_no = 0
    word_split = list(word)
    for choice in word_list_split:
        for index, correct_letter in enumerate(array):
            if correct_letter == 2:
                if choice[index] == word_split[index]:
                    pass
                else:
                    break
            elif correct_letter ==1:
                if choice[index] == word_split[index]:
                    break 
                elif choice[index] in word_split:
                    pass
                else:
                    break
            else:
                if choice[index] not in word_split:
                    pass
                else:
                    break
            if index == 4:
                total_no += 1

    return total_no

def possible_words(array, word, word_list_split):
    possible_word_list = []
    word_split = list(word)
    for choice in word_list_split:
        for index, correct_letter in enumerate(array):
            if correct_letter == 2:
                if choice[index] == word_split[index]:
                    pass
                else:
                    break
            elif correct_letter ==1:
                if choice[index] == word_split[index]:
                    break 
                elif word_split[index] in choice:
                    pass
                else:
                    break
            else:
                if word_split[index] not in choice:
                    pass
                else:
                    break
            if index == 4:
                possible_word_list.append(''.join(choice))
    return possible_word_list

def entropy(word, word_list):
    word_list_split = split_word_list(word_list)
    total_number = len(allowable_guesses)
    expected_value = 0
    permutations = generate_permutations(word)
    for permutation in permutations:
        no_words = possible_words_number_s(permutation, word, word_list_split)
        p = no_words/total_number
        if p != 0:
            expected_value += p*np.log2(1/p)
    return [word,expected_value]

if __name__ == "__main__":
    '''
    start = time.time()
    with Pool(os.cpu_count()-1) as p:
        data = p.map(entropy, allowable_guesses)
    np.savetxt("entropyrest.csv", data, delimiter = ',', fmt = '% s')
    end = time.time()
    print(end-start)
    '''

word = input('Enter the five letter word you put: ') 
correctness_array = list(map(int,list(input('Enter the correctness array: '))))
word_list = possible_words(correctness_array,word, allowable_guesses_split)
word_list_split = split_word_list(word_list)
new_list = []
for wd in word_list:
    new_list.append(entropy(wd,word_list))
print(pd.DataFrame(new_list).sort_values(1, ascending=False))
while 1:
    word = input('Enter a five letter word you put: ')
    correctness_array = list(map(int,list(input('Enter the correctness array: '))))
    word_list = possible_words(correctness_array, word, word_list_split)
    word_list_split = split_word_list(word_list)
    new_list = []
    for wd in word_list:
        new_list.append(entropy(wd,word_list))
    print(pd.DataFrame(new_list).sort_values(1, ascending=False))