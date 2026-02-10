# bhuviprojects
#🎮 Smart Number Guessing Game (Python)
#📖 Project Description
The Smart Number Guessing Game is a console-based Python application where the player tries to guess a randomly generated number within a limited number of attempts.
The game includes difficulty levels, an AI-based hint system, and a persistent scoreboard stored in a file.

This project is designed to work in any environment without requiring a graphical display, making it suitable for Linux servers, VS Code, GitHub Codespaces, and Windows.

#✨ Features
🎯 Random number generation
🧠 AI-based intelligent hints
📊 Persistent scoreboard using file handling
🎚 Multiple difficulty levels
🔁 Replayable game loop
🖥 Console-based (no GUI / no Flask)

#🛠 Technologies Used
Python 3
Built-in libraries:
random – number generation
os – file existence checks
time – delays for better UX

#📂 Code Structure Explanation
#1️⃣ Imports and Constants
import random
import os
import time
SCORE_FILE = "scores.txt"

random generates the secret number
os checks if the score file exists
time adds small pauses for better user experience
SCORE_FILE stores player scores persistently

#2️⃣ Score System
Saving Scores
def save_score(name, score, level):

Saves player name, score, and difficulty level
Uses file handling (append mode) so data is not overwritten

Displaying Scores
def show_scores():

Reads scores from scores.txt
Displays all previous players’ scores in a formatted table

#3️⃣ AI Hint System
def ai_hint(secret, guess):

The AI hint system helps the player by analyzing how close their guess is to the secret number:

Difference	            Hint Given
0	                    Perfect guess
≤ 5	                    Very close
≤ 10	                Close
Lower than secret	    Too low
Higher than secret	    Too high

This makes the game more interactive and intelligent.

#4️⃣ Game Logic
def play_game():

This function controls the entire gameplay:
Takes player name input
Allows difficulty selection:
Easy: 1–50 (10 attempts)
Medium: 1–100 (7 attempts)
Hard: 1–200 (5 attempts)
Generates a random number
Accepts guesses with error handling
Calculates score based on remaining attempts
Saves results to the scoreboard

#5️⃣ Main Menu System
def main():

The menu-driven interface allows the user to:
Play the game
View scoreboard
Exit the application
The loop ensures the user can play multiple times without restarting the program.

#6️⃣ Program Entry Point
if __name__ == "__main__":
    main()

This ensures the program runs correctly when executed directly and follows Python best practices.

#▶️ How to Run the Project
Step 1: Clone the Repository
git clone https://github.com/your-username/Smart-Number-Guessing-Game.git
cd Smart-Number-Guessing-Game

Step 2: Run the Program
python smart_number_game.py
