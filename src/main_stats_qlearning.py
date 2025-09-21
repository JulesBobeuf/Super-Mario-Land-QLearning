import pymongo
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

import database as db
from constants import *
import argparse


def plot_rewards(epochs, rewards, max_progress, attributes, document_key):
    plt.figure(figsize=(10, 5))
    plt.plot(epochs, rewards, marker='o', markersize=3, linestyle='-', alpha=0.6, color='b', label='Total Reward')
    plt.title(f"Reward for Document {document_key}")
    if (DISPLAY_MAX_PROGRESS):
        plt.plot(epochs, max_progress, marker='s', linestyle='--', color='r', label='Max Level Progress')
        plt.title(f"Reward & Level Progression for Document {document_key}")
    plt.xlabel("Epoch")
    plt.ylabel("Value")
    plt.legend()
    plt.grid()
    
    # Reduce the number of X-axis labels dynamically
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=8))
    
    # Display additional attributes as text on the plot
    attr_text = "\n".join([f"{k}: {v}" for k, v in attributes.items()])
    plt.gcf().text(0.01, 0.65, attr_text, fontsize=10, bbox=dict(facecolor='white', alpha=0.5))
    
    # Adjust the plot so that it looks good right away
    plt.subplots_adjust(left=0.192, bottom=0.11, right=0.99, top=0.88, wspace=0.2, hspace=0.2)
    plt.show()
    
    
def parse_args():
    """ Function to parse command-line arguments. """
    parser = argparse.ArgumentParser(description="Training the Q-learning agent on Super Mario Land.")
    parser.add_argument('--load', type=int, default=-1, help="Which key to load. Specify the _id")
    parser.add_argument('--even', action='store_true', help="Plot 4 graphs with even scaling")
    parser.add_argument('--mode', choices=['progress', 'reward'], default='progress', help="Which metric to graph")
    return parser.parse_args()

def graph_training(key:str):
    mongo = db.get_mongo_collection(DB_COLLECTION_QLEARNING)
    document = db.load(mongo, key)
    stats = document["stats"]
    stats = {int(k): v for k, v in document["stats"].items() if int(k) <= MAX_EPOCHS} #max 500

    epochs = sorted(stats.keys(), key=int) 
    rewards = [stats[epoch]["total_reward"] for epoch in epochs if "total_reward" in stats[epoch]]
    max_progress = [stats[epoch]["max_level_progress"] for epoch in epochs if "max_level_progress" in stats[epoch]]

    # Extract additional attributes to display on the plot
    excluded_keys = {"mapping", "incr", "stats"}
    attributes = {k: v for k, v in document.items() if k not in excluded_keys}

    if epochs and rewards:
        plot_rewards(epochs, rewards, max_progress, attributes, key)
    else:
        print("No valid data found to plot.")
        
        

def graph_run(key:str):
    mongo = db.get_mongo_collection(DB_COLLECTION_QL_RUN)
    data = list(mongo.find({"qlearning_id": key}))

    max_level_progress_values = [entry["max_level_progress"] for entry in data]
    total_reward_values = [entry["total_reward"] for entry in data]

    bins = np.arange(0, max(max(max_level_progress_values, default=0), max(total_reward_values, default=0)) + 100, 100)

    plt.figure(figsize=(12, 5))

    # Histogram max_level_progress
    plt.subplot(1, 2, 1)
    plt.hist(max_level_progress_values, bins=bins, color='blue', alpha=0.7, edgecolor='black')
    plt.xlabel("Max Level Progress (ranges of 100)")
    plt.ylabel("Count")
    plt.title("Max Level Progress Distribution")
    plt.xticks(bins, rotation=45)

    # Histogram total_reward
    plt.subplot(1, 2, 2)
    plt.hist(total_reward_values, bins=bins, color='green', alpha=0.7, edgecolor='black')
    plt.xlabel("Total Reward (ranges of 100)")
    plt.ylabel("Count")
    plt.title("Total Reward Distribution")
    plt.xticks(bins, rotation=45)
        
    plt.tight_layout()
    plt.show()

def graph_even_distribution(keys, mode='progress'):
    mongo = db.get_mongo_collection(DB_COLLECTION_QL_RUN)
    all_values = []

    data_per_key = {}
    for key in keys:
        data = list(mongo.find({"qlearning_id": key}))
        values = [entry["max_level_progress"] if mode == 'progress' else entry["total_reward"] for entry in data]
        data_per_key[key] = values
        all_values.extend(values)

    if not all_values:
        print("No data found to plot.")
        return

    max_val = max(all_values)
    bins = np.arange(0, ((max_val // 100) + 2) * 100, 100)

    ymax = 0
    for values in data_per_key.values():
        counts, _ = np.histogram(values, bins=bins)
        this_max = max(counts, default=0)
        ymax = max(ymax, this_max)
    ymax = int(ymax * 1.1) + 1

    fig, axes = plt.subplots(2, 2, figsize=(14, 8), constrained_layout=True)
    axes = axes.flatten()

    for i, key in enumerate(keys):
        values = data_per_key[key]
        ax = axes[i]
        ax.hist(values, bins=bins, color='royalblue', alpha=0.8, edgecolor='black')
        ax.set_title(f"{'Progress' if mode == 'progress' else 'Reward'} - Model {key}", fontsize=10)
        ax.set_xlabel("Value", fontsize=9)
        ax.set_ylabel("Count", fontsize=9)
        ax.set_ylim(0, ymax)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.set_xticks(bins)
        ax.tick_params(axis='x', rotation=45, labelsize=8)
        ax.tick_params(axis='y', labelsize=8)
        ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=5, integer=True))

    for j in range(i + 1, 4):
        fig.delaxes(axes[j])

    fig.suptitle(f"{'Max Level Progress' if mode == 'progress' else 'Total Reward'} Distributions", fontsize=14)
    plt.show()

def main():
    args = parse_args()

    if args.even:
        keys = ['1', '2', '3', '4']
        graph_even_distribution(keys, mode=args.mode)
        return

    key = '1'
    if args.load != -1:
        key = str(args.load)

    graph_run(key)



if __name__ == "__main__":
    main()