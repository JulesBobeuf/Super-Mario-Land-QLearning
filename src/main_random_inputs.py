from pyboy import PyBoy

import random
from constants import *

pyboy = PyBoy('../sml.gb')
pyboy.set_emulation_speed(1) # Default speed

mario = pyboy.game_wrapper
mario.game_area_mapping(mario.mapping_compressed, 0)

def play_random_input():
    """Presses a random button from the inputs list."""
    random_input = random.choice(INPUTS)
    pyboy.button(random_input)


if __name__ == "__main__":
    mario.start_game()
    last_time = mario.time_left
    try:
        for _ in range(1000):
            #play_random_input()
            pyboy.tick()  # Advance one frame

    finally:
        print("\nfull map :\n")
        print(mario)
        print("\nmap compressed :\n")
        print(mapping_compressed)
        pyboy.stop()