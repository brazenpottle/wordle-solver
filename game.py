#####-----A Wordle Clone-----#####
from operator import mod
import numpy as np
from preprocessing import allowable_guesses, possible_answers

# define constants
MAX_GUESSES = 6

# round function
def play_round(answer, guess):
    '''
    INPUTS:     answer:             a 5 character string that must be found in possible_answers.txt
                guess:              a 5 character string that must be found in allowable_guesses.txt
    
    OUTPUTS:    correctness_array:  array of 5 ints representing the correctness of each guess (see README)
    '''

    correctness_array = np.zeros(5)
    
    valid_guess = (guess in allowable_guesses)
    while not valid_guess:
        print("Error: guess must be in allowable_guesses.txt")
        guess = input("Please provide a valid guess: ")
        valid_guess = (guess in allowable_guesses)
    
    checked = []
    i = 0
    while i < len(guess):
        if guess[i] in answer and not guess[i] in checked:
            correctness_array[i] = 1

        checked.append(guess[i])

        i += 1

    i = 0
    while i < len(guess):
        if guess[i] == answer[i]:
            correctness_array[i] = 2
        
        i += 1        

    correctness_array = correctness_array.astype(int)
    
    return correctness_array

# game function
def play_game(answer=None):
    '''
    INPUTS:     answer:             a 5 character string that must be found in possible_answers.txt

    OUTPUTS:    user_guesses:       array of 6 strings representing the guesses made by the user
                correctness_arrays: int array of shape (6, 5) representing the correctness of each guess by the user (see README)
                score:              int representing how many guesses the user made before winning.
                                    If the user failed, returns 0
    '''
    
    if answer == None:
        # pick a random word from allowable_guesses
        pass
    if not answer in possible_answers:
        print("Error: answer must be in possible_answers.txt")
        print("Terminating program.")
        exit(1)

    user_guesses = []
    correctness_arrays = np.ndarray((6, 5))
    
    score = 1
    for i in range(MAX_GUESSES):
        guess = input("Guess: ").strip("\n")
        user_guesses.append(guess)
        if guess == answer:
            break
        
        # provide hint
        correctness_array = play_round(answer, guess)
        correctness_arrays[i] = correctness_array
        
        print(correctness_array)

        score += 1

    if score > 6:
        score = 0

    if score == 0:
        print("The word was: " + answer)
        print("Better luck next time.")
    else:
        print("Congratulations.")
        print("You took {} guesses.".format(score))

    return (user_guesses, correctness_arrays, score)

if __name__ == "__main__":
    # play a sample game
    play_game(possible_answers[42])