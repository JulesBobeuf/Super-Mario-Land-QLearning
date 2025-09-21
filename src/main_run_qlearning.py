import argparse
from constants import *
from qLearning.run import run


def parse_args():
    """ Function to parse command-line arguments. """
    parser = argparse.ArgumentParser(description="Training the Q-learning agent on Super Mario Land.")
    parser.add_argument('--load', type=int, default=-1, help="Load a pre-existing model to resume training. Specify the _id")
    return parser.parse_args()

def main():
    """ Main entry point to start training. """
    # Parse arguments
    args = parse_args()

    # Pass arguments to the training function (in train.py)
    print("Starting training with the following parameters:")
    print(f"  - Loading a pre-existing model: {args.load}")
    
    # run
    run(load=str(args.load))
    
    
if __name__ == "__main__":
    main()
