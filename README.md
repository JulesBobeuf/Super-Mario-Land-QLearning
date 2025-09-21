# Super-Mario-Land-QLearning

<video src="marioooooo.mp4" controls width="600"></video>

**Super-Mario-Land-QLearning** is a university project in which we created an AI to play **Super Mario Land** using reinforcement learning techniques.

## About The Project

The goal of this project was to design an AI capable of playing Super Mario Land effectively. The AI is trained using Q-learning and is able to navigate levels autonomously.

## Built With

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)  

## Getting Started

### Folder Structure

```markdown
Super-Mario-Land-QLearning/
├── 📁 src/                       # Source code for AI and game logic
│   ├── 📁 qLearning/             # Q-learning implementation
│   ├── 📄 constants.py           # Project constants and settings
│   ├── 📄 database.py            # Database for storing training data
│   ├── 📄 main_random_inputs.py  # Run AI with random inputs
│   ├── 📄 main_run_qlearning.py  # Run AI using Q-learning
│   ├── 📄 main_stats_qlearning.py# Generate statistics from Q-learning runs
│   └── 📄 main_train_qlearning.py# Train the Q-learning agent
├── 📄 requirements.txt           # Python dependencies
├── 📄 sml.gb                      # Super Mario Land game ROM
├── 📄 marioooooo.mp4             # Demo video of the AI playing
├── 📄 ARTICLE_SUPER_MARIO.pdf    # Project report
└── 📄 LICENSE                    # MIT License
```

### Prerequisites

Ensure you have Python 3.10+ installed.

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running the AI

1. Activate the virtual environment:

```sh
source .venv/bin/activate
```

2. Run the Q-learning AI:

```sh
python src/main_run_qlearning.py
```

3. Observe the AI playing Super Mario Land autonomously.

## Usage

The AI will interact with the ROM and display gameplay while learning optimal moves using Q-learning. 

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

Jules Bobeuf  
[LinkedIn](https://www.linkedin.com/in/bobeuf-jules/)  
bobeuf.jules@gmail.com

Valentin Devisme  
[LinkedIn](https://www.linkedin.com/in/valentin-devisme-42003728b/)  
