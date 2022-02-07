# A basic simulation of wordle

def run(lines=-1):
    MAX_NUM_OF_SIMS = sum(1 for line in open("data/possible_answers.txt")) 
    num_of_sims = None
    
    if lines < 0:
        # run simulation on all of data/possible_answers.txt
        num_of_sims = MAX_NUM_OF_SIMS
    elif lines <= MAX_NUM_OF_SIMS:
        num_of_sims = lines
    else:
        print("Cannot run more simulations than number of possible answers!")
        return None