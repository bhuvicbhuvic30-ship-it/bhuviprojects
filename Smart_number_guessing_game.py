# =========================
# SMART NUMBER GUESSING GAME
# =========================

import random, os, time, hashlib, sqlite3
from datetime import datetime

# -------- GUI --------
import tkinter as tk
from tkinter import messagebox

# -------- WEB --------
from flask import Flask, render_template_string, request, redirect, session

# -------- SOUND (Windows) --------
try:
    import winsound
    SOUND = True
except:
    SOUND = False

DB_FILE = "game.db"
current_user = None
is_dark = False

# =========================
# DATABASE
# =========================

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT,
        games INTEGER,
        best INTEGER,
        total INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS scores(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        score INTEGER,
        date TEXT,
        time TEXT
    )
    """)

    conn.commit()
    conn.close()

# =========================
# UTILITIES
# =========================

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def play_sound(t):
    if not SOUND:
        return
    if t == "win":
        winsound.Beep(1200, 300)
    elif t == "lose":
        winsound.Beep(400, 500)

def smart_hint(secret, guess):
    diff = abs(secret - guess)
    if diff == 0:
        return "🎯 Perfect!"
    elif diff <= 2:
        return "🔥 Extremely Close!"
    elif diff <= 5:
        return "✨ Very Close!"
    elif guess < secret:
        return "📉 Too Low!"
    else:
        return "📈 Too High!"

def adaptive_difficulty(best):
    if best > 80:
        return 100, 8
    elif best < 30:
        return 20, 10
    return 50, 7

# =========================
# DATABASE OPERATIONS
# =========================

def save_score(user, score):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    now = datetime.now()

    cur.execute(
        "INSERT INTO scores(username,score,date,time) VALUES (?,?,?,?)",
        (user, score, now.strftime("%d-%m-%Y"), now.strftime("%H:%M:%S"))
    )

    cur.execute("""
    UPDATE users
    SET games = games + 1,
        total = total + ?,
        best = MAX(best, ?)
    WHERE username = ?
    """, (score, score, user))

    conn.commit()
    conn.close()

def get_best_score(user):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT best FROM users WHERE username=?", (user,))
    r = cur.fetchone()
    conn.close()
    return r[0] if r else 0

# =========================
# LOGIN WINDOW
# =========================

def login_window():
    global current_user

    win = tk.Toplevel(root)
    win.title("Login")

    tk.Label(win, text="Username").pack()
    u = tk.Entry(win)
    u.pack()

    tk.Label(win, text="Password").pack()
    p = tk.Entry(win, show="*")
    p.pack()

    def login():
        global current_user
        user = u.get()
        pw = hash_password(p.get())

        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE username=?", (user,))
        r = cur.fetchone()

        if r:
            if r[0] == pw:
                current_user = user
                messagebox.showinfo("Success", "Login Successful")
                win.destroy()
            else:
                messagebox.showerror("Error", "Wrong Password")
        else:
            cur.execute(
                "INSERT INTO users VALUES (?,?,?,?,?)",
                (user, pw, 0, 0, 0)
            )
            conn.commit()
            current_user = user
            messagebox.showinfo("Registered", "Account Created")
            win.destroy()

        conn.close()

    tk.Button(win, text="Login / Register", command=login).pack(pady=10)

# =========================
# GAME LOGIC (GUI)
# =========================

def start_game():
    if not current_user:
        messagebox.showerror("Error", "Please login first")
        return

    best = get_best_score(current_user)
    max_num, attempts = adaptive_difficulty(best)
    secret = random.randint(1, max_num)
    start = time.time()

    for i in range(1, attempts + 1):
        guess = simple_input(f"Attempt {i}/{attempts}\nGuess 1–{max_num}")
        if guess is None:
            return

        if guess == secret:
            elapsed = int(time.time() - start)
            score = max(0, (attempts - i + 1) * 10 - elapsed)
            save_score(current_user, score)
            play_sound("win")
            messagebox.showinfo("Win", f"🎉 Correct!\nScore: {score}")
            return
        else:
            messagebox.showinfo("Hint", smart_hint(secret, guess))

    save_score(current_user, 0)
    play_sound("lose")
    messagebox.showinfo("Game Over", f"Number was {secret}")

def simple_input(text):
    w = tk.Toplevel(root)
    w.title("Input")
    tk.Label(w, text=text).pack()
    e = tk.Entry(w)
    e.pack()

    val = {"x": None}

    def submit():
        try:
            val["x"] = int(e.get())
            w.destroy()
        except:
            messagebox.showerror("Error", "Enter number only")

    tk.Button(w, text="Submit", command=submit).pack()
    w.wait_window()
    return val["x"]

# =========================
# LEADERBOARD & STATS
# =========================

def show_leaderboard():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
    SELECT username, MAX(score)
    FROM scores
    GROUP BY username
    ORDER BY MAX(score) DESC
    """)
    rows = cur.fetchall()
    conn.close()

    text = "🏆 Leaderboard\n\n"
    for i, r in enumerate(rows, 1):
        text += f"{i}. {r[0]} - {r[1]}\n"

    messagebox.showinfo("Leaderboard", text)

def show_stats():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT games,best,total FROM users WHERE username=?", (current_user,))
    g, b, t = cur.fetchone()
    conn.close()

    avg = t // g if g else 0
    messagebox.showinfo(
        "My Stats",
        f"User: {current_user}\nGames: {g}\nBest: {b}\nAverage: {avg}"
    )

# =========================
# THEME
# =========================

def toggle_theme():
    global is_dark
    is_dark = not is_dark
    bg = "#1e1e1e" if is_dark else "#f0f0f0"
    fg = "white" if is_dark else "black"
    root.configure(bg=bg)
    for w in root.winfo_children():
        try:
            w.configure(bg=bg, fg=fg)
        except:
            pass

# =========================
# GUI
# =========================

init_db()
root = tk.Tk()
root.title("Smart Number Guessing Game")
root.geometry("420x520")

tk.Label(root, text="🎮 Smart Number Guessing Game",
         font=("Segoe UI", 18, "bold")).pack(pady=15)

tk.Button(root, text="🔐 Login / Register", command=login_window).pack()
tk.Button(root, text="▶ Play Game", command=start_game).pack(pady=10)
tk.Button(root, text="🏆 Leaderboard", command=show_leaderboard).pack()
tk.Button(root, text="📊 My Stats", command=show_stats).pack()
tk.Button(root, text="🌙 Toggle Dark Mode", command=toggle_theme).pack(pady=5)
tk.Button(root, text="❌ Exit", command=root.destroy).pack(pady=15)

root.mainloop()
