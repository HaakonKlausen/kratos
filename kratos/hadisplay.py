import datetime
from os import stat_result
import pytz
import tkinter as tk
import tkinter.font as tkFont
import time
import datetime 
import sys

# Default font size
font_size = -12

class HaDisplay(tk.Frame):
    def __init__(self):
        # Create the main window
        self.__root = tk.Tk()
        self.__root.title("Kratosdisplay")

        # Create the main container
        self.__frame = tk.Frame(self.__root, bg='black')

        # Variables for holding temperature and light data
        self.__dtime = tk.StringVar()
        self.__ddate = tk.StringVar()
        # Variable for holding temperature data
        dtemp = tk.StringVar()

        dcottagetemp = tk.StringVar()
        dcottagetempinside = tk.StringVar()
        dcottageactivepower = tk.StringVar()

        dtempinside = tk.StringVar()
        dsymbolcode = tk.StringVar()

        dpowerprice = tk.StringVar()
        dmaxpowerprice = tk.StringVar()

        dactivepower = tk.StringVar()
        dactarget = tk.StringVar()
        dchargertarget = tk.StringVar()

        # Create dynamic font for text
        temp_dfont = tkFont.Font(family='Helvetica', size=-36)
        time_dfont = tkFont.Font(family='Helvetica', size=-8)
        date_dfont = tkFont.Font(family='Helvetica', size=-8)

        button_dfont = tkFont.Font(size=font_size)

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

if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    root.title("Kratosdisplay")

    # Create the main container
    frame = tk.Frame(root, bg='black')
    display = HaDisplay(frame)
