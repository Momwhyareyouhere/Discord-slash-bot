import tkinter as tk
from tkinter import filedialog, scrolledtext
import subprocess
import os
import threading

class BotController:
    def __init__(self, root):
        self.root = root
        self.root.title("Bot Controller")


        self.start_button = tk.Button(root, text="Start Bot", command=self.start_bot)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Bot", command=self.stop_bot)
        self.stop_button.pack(pady=10)


        self.console = scrolledtext.ScrolledText(root, width=50, height=10)
        self.console.pack(padx=10, pady=10)


        self.bot_process = None
        self.bot_thread = None

    def start_bot(self):
        if self.bot_process is None and (self.bot_thread is None or not self.bot_thread.is_alive()):
            self.print_to_console("Starting bot...")
            try:
                self.bot_thread = threading.Thread(target=self.run_bot)
                self.bot_thread.start()
            except Exception as e:
                self.print_to_console(f"Error starting bot: {str(e)}")
        else:
            self.print_to_console("Bot is already running.")

    def run_bot(self):
        try:
            self.bot_process = subprocess.Popen(["python", "bot.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, universal_newlines=True)
            while self.bot_process.poll() is None:
                output = self.bot_process.stdout.readline()
                if output:
                    self.print_to_console(output.strip())
            self.print_to_console("Bot stopped.")
        except Exception as e:
            self.print_to_console(f"Error running bot: {str(e)}")
        finally:
            self.bot_process = None
            self.bot_thread = None

    def stop_bot(self):
        if self.bot_thread and self.bot_thread.is_alive():
            self.print_to_console("Stopping bot...")
            self.bot_process.terminate()
            self.bot_thread.join()
        else:
            self.print_to_console("Bot is not running.")
        self.bot_thread = None

    def print_to_console(self, message):
        self.console.insert(tk.END, message + "\n")
        self.console.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = BotController(root)
    root.mainloop()
