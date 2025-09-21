import numpy as np

# Global

<<<<<<< HEAD
SIZE_MATRIX = (16,20)

# Mario and Daisy
base_scripts = list(range(81))
plane = list(range(99, 110))
submarine = list(range(112, 122))

# Mario shoots
shoots = [96, 110, 122]

# Bonuses
coin = [244]
mushroom = [131]
heart = [132]
star = [134]
flower = [224, 229]

# Lever for level end
lever = [255]

# Solid blocks
neutral_blocks = [
    142, 143, 221, 222, 231, 232, 233, 234, 235, 236, 301, 302, 303, 304, 319, 340, 352, 353, 355, 356, 357, 358, 359,
    360, 361, 362, 381, 382, 383
]
moving_blocks = [230, 238, 239]
pushable_blokcs = [128, 130, 354]
question_block = [129]
pipes = list(range(368, 381))

# Enemies
goomba = [144]
koopa = [150, 151, 152, 153]
plant = [146, 147, 148, 149]
moth = [160, 161, 162, 163, 176, 177, 178, 179]
flying_moth = [192, 193, 194, 195, 208, 209, 210, 211]
sphinx = [164, 165, 166, 167, 180, 181, 182, 183]
big_sphinx = [198, 199, 201, 202, 203, 204, 205, 214, 215, 217, 218, 219]
fist = [240, 241, 242, 243]
bill = [249]
projectiles = [172, 188, 196, 197, 212, 213, 226, 227]
shell = [154, 155]
explosion = [157, 158]
spike = [237]

ennemies = [goomba, koopa, plant, moth, flying_moth, sphinx, big_sphinx, fist, bill, shell, explosion, spike]
projectiles = [projectiles]
solid_blocks = [neutral_blocks, moving_blocks, question_block, pipes]
bonuses = [coin, mushroom, heart, star]
mario_shoot = [shoots]

categories = [ennemies, projectiles, solid_blocks, bonuses, mario_shoot]
category_names = ["enemies", "projectiles", "solid_blocks", "bonuses", "mario_shoot"]

TILES = 384

mapping_compressed = np.zeros(TILES, dtype=np.uint8)
compressed_list = [
    base_scripts, plane, submarine, shoots, coin, mushroom, heart, star, lever, neutral_blocks, moving_blocks,
    pushable_blokcs, question_block, pipes, goomba, koopa, plant, moth, flying_moth, sphinx, big_sphinx, fist, bill,
    projectiles, shell, explosion, spike
]
for i, tile_list in enumerate(compressed_list):
    for tile in tile_list:
        mapping_compressed[tile] = i + 1


# a = jump, left = move back, right = move forward
INPUTS:list = ['a', 'right', 'left']
=======
# right = move forward, a = jump, left = move back
INPUTS:list = ['right', 'a', 'left', 'longjump']
>>>>>>> af7a3f36b9fd513b3cdfcceafed2e04bcec7b4fb

ALL_INPUTS:list = ['up', 'down', 'left', 'right', 'a', 'b', 'start', 'select']

# Qlearning

QL_EPOCHS:int = 10000
QL_TICKS:int = 10_000
QL_SPEED:int = 100

## Q learning constants
QL_LEARNING_RATE:float = 0.001
QL_GAMMA:float = 0.99

# Greedy Epsilon
QL_DECREASE_EPSILON:bool = False
QL_EPSILON:float = 0.1
QL_EPSILON_DECAY:float = 0.001
QL_EPSILON_MIN:float = 0

# State size
QL_STATE_HEIGHT:int = 10
QL_STATE_WIDTH:int = 10

# Run
QL_RUNS:int = 500

# Database

DB_HOST:str = "http://localhost:27017"

DB_NAME:str = "mario"

DB_COLLECTION_QLEARNING:str = "qlearning"
DB_COLLECTION_QTABLE:str = "qtable"
DB_COLLECTION_QL_RUN:str = "ql_run"
DB_COLLECTION_QL_MAPPING:str = "ql_mapping"

# Stats

DISPLAY_MAX_PROGRESS:bool = False
MAX_EPOCHS:int = 500
