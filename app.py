import os
import threading
from flask import Flask
# Import your bot's main execution function if it's modular, 
# or use subprocess/os to run it as a script.
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return "MasterGen Service is Active and Running!"

def run_bot():
    # This runs your bot.py script in the background
    try:
        subprocess.run(["python3", "bot.py"], check=True)
    except Exception as e:
        print(f"Error running bot: {e}", flush=True)

if __name__ == "__main__":
    # Start the bot in a separate background thread so it doesn't block the port
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    # Start the Flask web server required by Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
