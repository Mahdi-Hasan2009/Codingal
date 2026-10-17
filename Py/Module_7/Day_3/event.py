"""

Write a Python Tkinter program that creates a 300x200 window titled "Security Trap". Bind events to the window so that left-clicking the mouse anywhere displays a warning pop-up saying "Intruder Detected", while pressing the Enter key displays an info pop-up saying "Access Granted"

"""

from tkinter import *
from tkinter import messagebox

# Setup Tkinter Window
root = Tk()
root.title("Security Trap")    
root.geometry("300x200")        

def intruder(event):
    messagebox.showwarning("Warning", "Intruder Detected")
def access(event):
    messagebox.showinfo("Info", "Access Granted")

root.bind("<Button-1>", intruder)

root.bind("<Return>", access)
root.mainloop()
