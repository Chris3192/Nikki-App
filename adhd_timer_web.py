import os
from pyngrok import ngrok
from flask import Flask, render_template
import threading
import time
import random

app = Flask(__name__)

# Encouragement messages
messages = [
    "You're doing great! Keep going! 💪",
    "Stay focused, you're making progress! 🚀",
    "One step at a time. You've got this! 🎯",
    "Breathe. You're in control. 🌿",
    "Your work matters. Keep pushing! 🔥"
]

timer_data = {
    "time_left": 25 * 60,
    "running": False,
    "paused": False,
    "message": ""
}

# This event will be used to control the pause/resume functionality
pause_event = threading.Event()
pause_event.set()  # Initially allow the countdown to run

def countdown():
    """Background thread for the timer countdown."""
    while timer_data["running"]:
        if timer_data["time_left"] > 0:
            # Check if the timer is paused, if so, wait until it is resumed
            pause_event.wait()  # If the event is cleared, it will block here
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
        timer_data["time_left"] = 25 * 60  # Reset timer
        timer_data["message"] = ""
        threading.Thread(target=countdown, daemon=True).start()
    return "Timer started!"

@app.route("/pause")
def pause_timer():
    if timer_data["running"]:
        timer_data["paused"] = not timer_data["paused"]
        if timer_data["paused"]:
            pause_event.clear()  # Block the countdown
        else:
            pause_event.set()  # Resume the countdown
    return "Timer paused/resumed!"

@app.route("/reset")
def reset_timer():
    timer_data["running"] = False
    timer_data["paused"] = False
    timer_data["time_left"] = 25 * 60
    timer_data["message"] = ""
    pause_event.set()  # Make sure the countdown is not blocked
    return "Timer reset!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Default to 10000 if PORT is not set
    app.run(host='0.0.0.0', port=port)






