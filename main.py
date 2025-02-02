import sys
import os

# Ensure the script recognizes subdirectories as packages
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import functions from the scene files
from openingScene.openingScene import run_opening_scene
from miniGame.miniGame import run_mini_game
from endingScene.endingScene import run_ending_scene

def main():
    run_opening_scene()  # Start the opening scene
    run_mini_game()      # Automatically start the mini-game
    run_ending_scene()   # Show the ending scene

if __name__ == "__main__":
    main()  # Run the full game sequence

