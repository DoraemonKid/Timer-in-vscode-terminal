import time
import os
import subprocess
import sys
import tty
import termios
import threading


key = ""
level = 50 
running = True
# Get user input for time
amountOfTime = input("Enter time in xx:xx:xx format: ")
hours, minutes, seconds = amountOfTime.split(":")

hours, minutes, seconds = int(hours), int(minutes), int(seconds)


def listen():
    # Save terminal settings
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd) # Don't wait for Enter key
        while True:
            key = sys.stdin.read(1)
            if key == 'p':
                global running
                running = False
            elif key == 'r':
                running = True
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def clear_terminal():
    # Use 'cls' for Windows, 'clear' for Linux/macOS
    os.system('clear' if os.name == 'nt' else 'clear')




# Run in background
threading.Thread(target=listen, daemon=True).start()

# Run the timer
timeLeft = hours * 3600 + minutes * 60 + seconds
clear_terminal()
seconds = seconds + 1
timeLeft += 1

while timeLeft > 0:
    if running:
        # Only decrease time and print if running is True
        print(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        print("Press 'p' to pause, 'r' to resume.")
        
        time.sleep(1)
        timeLeft -= 1
        seconds -= 1

        if seconds < 0:
            if minutes > 0 or hours > 0:
                seconds = 59
                if minutes > 0:
                    minutes -= 1
                else:
                    hours -= 1
                    minutes = 59
        
        clear_terminal()
    else:
        # If paused, just wait a bit and check again without losing time
        print("PAUSED - Press 'r' to resume.")
        time.sleep(0.1) 
        clear_terminal()

# Timer finished
print("Time's up")

for i in range(0, 5):
    subprocess.run(["afplay", "-v", "8", "/System/Library/Sounds/Submarine.aiff"])

clear_terminal()
