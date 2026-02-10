import random
import os
import time

SCORE_FILE = "scores.txt"

# ================== SCORE SYSTEM ==================
def save_score(name, score, level):
    with open(SCORE_FILE, "a") as f:
        f.write(f"{name},{score},{level}\n")

def show_scores():
    if not os.path.exists(SCORE_FILE):
        print("\n📊 No scores yet.\n")
        return

    print("\n📊 SCOREBOARD")
    print("-" * 30)
    with open(SCORE_FILE, "r") as f:
        for line in f:
            name, score, level = line.strip().split(",")
            print(f"{name} | Score: {score} | Level: {level}")
    print("-" * 30)

# ================== AI HINT SYSTEM ==================
def ai_hint(secret, guess):
    diff = abs(secret - guess)

    if diff == 0:
        return "🎯 Perfect! You got it."
    elif diff <= 5:
        return "🔥 Very close!"
    elif diff <= 10:
        return "🙂 Close, keep trying."
    elif guess < secret:
        return "📈 Too low."
    else:
        return "📉 Too high."

# ================== GAME LOGIC ==================
def play_game():
    print("\n🎮 SMART NUMBER GUESSING GAME 🎮")
    name = input("Enter your name: ").strip()

    print("\nChoose difficulty:")
    print("1. Easy   (1–50, 10 attempts)")
    print("2. Medium (1–100, 7 attempts)")
    print("3. Hard   (1–200, 5 attempts)")

    while True:
        choice = input("Select (1/2/3): ")
        if choice in ["1", "2", "3"]:
            break
        print("Invalid choice. Try again.")

    if choice == "1":
        max_num, attempts, level = 50, 10, "Easy"
    elif choice == "2":
        max_num, attempts, level = 100, 7, "Medium"
    else:
        max_num, attempts, level = 200, 5, "Hard"

    secret = random.randint(1, max_num)

    print(f"\nI picked a number between 1 and {max_num}")
    print(f"You have {attempts} attempts.\n")

    for attempt in range(1, attempts + 1):
        try:
            guess = int(input(f"Attempt {attempt}/{attempts}: "))
        except ValueError:
            print("❌ Enter a valid number.")
            continue

        hint = ai_hint(secret, guess)
        print(hint)

        if guess == secret:
            score = (attempts - attempt + 1) * 10
            print(f"\n🏆 Congratulations {name}! Your score: {score}")
            save_score(name, score, level)
            return

    print(f"\n💀 Game Over! The number was {secret}")
    save_score(name, 0, level)

# ================== MAIN MENU ==================
def main():
    while True:
        print("\n========== MAIN MENU ==========")
        print("1. Play Game")
        print("2. View Scoreboard")
        print("3. Exit")

        choice = input("Choose: ")

        if choice == "1":
            play_game()
        elif choice == "2":
            show_scores()
        elif choice == "3":
            print("\n👋 Thanks for playing!")
            break
        else:
            print("❌ Invalid option.")

        time.sleep(1)

# ================== ENTRY POINT ==================
if __name__ == "__main__":
    main()
