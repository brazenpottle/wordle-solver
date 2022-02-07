# A basic simulation of wordle
import time
import sys
import game
import os

# a fun progress bar
def percent_complete(step, total_steps, bar_width=60, title="", print_perc=True):
    # UTF-8 left blocks: 1, 1/8, 1/4, 3/8, 1/2, 5/8, 3/4, 7/8
    utf_8s = ["█", "▏", "▎", "▍", "▌", "▋", "▊", "█"]
    perc = 100 * float(step) / float(total_steps)
    max_ticks = bar_width * 8
    num_ticks = int(round(perc / 100 * max_ticks))
    full_ticks = num_ticks / 8      # Number of full blocks
    part_ticks = num_ticks % 8      # Size of partial block (array index)
    
    disp = bar = ""                 # Blank out variables
    bar += utf_8s[0] * int(full_ticks)   # Add full blocks into Progress Bar
    
    # If part_ticks is zero, then no partial block, else append part char
    if part_ticks > 0:
        bar += utf_8s[part_ticks]
    
    # Pad Progress Bar with fill character
    bar += "▒" * int((max_ticks/8 - float(num_ticks)/8.0))
    
    if len(title) > 0:
        disp = title + ": "         # Optional title to progress display
    
    disp += bar                     # Progress bar to progress display
    if print_perc:
        # If requested, append percentage complete to progress display
        disp += " {} / {}".format(step + 1, total_steps)
    
    # Output to terminal repetitively over the same line using '\r'.
    sys.stdout.write("\r" + disp)
    sys.stdout.flush()



if __name__ == "__main__":
    num_of_sims = sum(1 for line in open("data/possible_answers.txt")) 
    
    with open("data/possible_answers.txt") as answers:
        i = 0
        for ans in answers:
            # no need to touch
            time.sleep(0.0001)
            os.system('clear')
            percent_complete(i, num_of_sims, title=ans.strip())
            print()

            ##----------------COMPLETE: the wordle game simulation------------##
            
            ##----------------------------------------------------------------##

            i += 1
        
        print("\nSimulation complete!")