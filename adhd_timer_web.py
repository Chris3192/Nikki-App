import os
from flask import Flask, render_template
import threading
import time
import random

app = Flask(__name__)

# Encouragement messages
messages = [
    "You're doing great Ms! Keep going! 💪",
    "Stay focused, you're making progress Puta! 🚀",
    "One step at a time. You've got this Capi Cheeks! 🎯",
    "Breathe. You're in control 🌿",
    "Your work matters. Keep pushing! 🔥"
]

timer_data = {
    "time_left": 25 * 60,
    "running": False,
    "paused": False,
    "message": ""
}

def countdown():
    """Background thread for the timer countdown."""
    while timer_data["running"]:
        if not timer_data["paused"] and timer_data["time_left"] > 0:
            time.sleep(1)
            timer_data["time_left"] -= 1

        if timer_data["time_left"] == 0:
            timer_data["running"] = False
            timer_data["message"] = random.choice(messages)
            break

@app.route("/")
def index():
    return render_template("index.html",
                           time_left=timer_data["time_left"],
                           message=timer_data["message"],
                           running=timer_data["running"],
                           paused=timer_data["paused"])

@app.route("/start")
def start_timer():
    if not timer_data["running"]:
        timer_data["running"] = True
        timer_data["paused"] = False
        timer_data["time_left"] = 25 * 60
        timer_data["message"] = "Timer started! Let's go Nikki! 🚀"
        threading.Thread(target=countdown, daemon=True).start()

    return render_template("index.html",
                           time_left=timer_data["time_left"],
                           message=timer_data["message"],
                           running=timer_data["running"],
                           paused=timer_data["paused"])

@app.route("/pause")
def pause_timer():
    if timer_data["running"]:
        timer_data["paused"] = not timer_data["paused"]
        if timer_data["paused"]:
            timer_data["message"] = "Timer paused. Don't be lazy Puta!! ☕"
        else:
            timer_data["message"] = "Timer resumed. Let's keep moving Capi Cheeks! 💨"

    return render_template("index.html",
                           time_left=timer_data["time_left"],
                           message=timer_data["message"],
                           running=timer_data["running"],
                           paused=timer_data["paused"])

@app.route("/reset")
def reset_timer():
    timer_data["running"] = False
    timer_data["paused"] = False
    timer_data["time_left"] = 25 * 60
    timer_data["message"] = "Timer reset! Lets have some Coca leafs! 🌿"

    return render_template("index.html",
                           time_left=timer_data["time_left"],
                           message=timer_data["message"],
                           running=timer_data["running"],
                           paused=timer_data["paused"])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
