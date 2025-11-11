import datetime
from os import stat_result
import pytz
import tkinter as tk
import tkinter.font as tkFont
import time
import datetime 
import sys


class HaDisplay(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg="black")
        self.timeFont = tkFont.Font(family="Helvetica", size=48, weight="bold")
        self.dateFont = tkFont.Font(family="Helvetica", size=24)
        self.tempFont = tkFont.Font(family="Helvetica", size=32)

        self.timeLabel = tk.Label(self, font=self.timeFont, fg="white", bg="black")
        self.timeLabel.pack(pady=(20, 0))

        self.dateLabel = tk.Label(self, font=self.dateFont, fg="white", bg="black")
        self.dateLabel.pack(pady=(10, 0))

        self.tempLabel = tk.Label(self, font=self.tempFont, fg="white", bg="black")
        self.tempLabel.pack(pady=(10, 20))

        self.update_display()

    def update_display(self):
        now = datetime.datetime.now(pytz.timezone('America/New_York'))
        current_time = now.strftime("%I:%M %p")
        current_date = now.strftime("%A, %B %d, %Y")

        # Simulated temperature reading
        current_temp = "72°F"

        self.timeLabel.config(text=current_time)
        self.dateLabel.config(text=current_date)
        self.tempLabel.config(text=f"Temp: {current_temp}")

        # Schedule the next update in 1 minute
        self.after(60000, self.update_display)