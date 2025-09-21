import argparse
from constants import *
from qLearning.train import train_agent


def parse_args():
    """ Function to parse command-line arguments. """
    parser = argparse.ArgumentParser(description="Training the Q-learning agent on Super Mario Land.")
    parser.add_argument('--load', type=int, default=-1, help="Load a pre-existing model to resume training. Specify the _id")
    parser.add_argument('--epochs', type=int, default=QL_EPOCHS, help="Number of epochs for training")
    parser.add_argument('--ticks', type=int, default=QL_TICKS, help="Number of ticks per epoch")
    parser.add_argument('--epsilon', type=float, default=QL_EPSILON, help="Initial epsilon value for exploration")
    parser.add_argument('--speed', type=int, default=QL_SPEED, help="Initial speed value for exploration")
    parser.add_argument('--state_height', type=int, default=QL_STATE_HEIGHT, help="Height of the state representation")
    parser.add_argument('--state_width', type=int, default=QL_STATE_WIDTH, help="Width of the state representation")
    parser.add_argument('--learning_rate', type=float, default=QL_LEARNING_RATE, help="Learning rate for Q-learning")
    parser.add_argument('--gamma', type=float, default=QL_GAMMA, help="Discount factor for future rewards")
    return parser.parse_args()

def main():
    """ Main entry point to start training. """
    # Parse arguments
    args = parse_args()

    # Pass arguments to the training function (in train.py)
    print("Starting training with the following parameters:")
    print(f"  - Loading a pre-existing model: {args.load}")
    print(f"  - Number of epochs: {args.epochs}")
    print(f"  - Number of ticks per epoch: {args.ticks}")
    print(f"  - Initial epsilon value: {args.epsilon}")
    print(f"  - State representation height: {args.state_height}")
    print(f"  - State representation width: {args.state_width}")
    print(f"  - Learning rate: {args.learning_rate}")
    print(f"  - Discount factor (gamma): {args.gamma}")
    
    # Call the training function with the arguments
    train_agent(
        load=str(args.load),
        epochs=args.epochs,
        ticks=args.ticks,
        epsilon=args.epsilon,
        state_height=args.state_height,
        state_width=args.state_width,
        learning_rate=args.learning_rate,
        gamma=args.gamma
    )
    
    
if __name__ == "__main__":
    main()
