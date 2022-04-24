import os
import game

os.system('python3 -m venv wordle && . wordle/bin/activate && pip install -r requirements.txt')

game.play_game("point")