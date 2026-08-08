import tkinter as tk

root = tk.Tk()
root.title("My first Tkinter window")
root.geometry("800x500")

label = tk.Label(root,text="Hi, Tkinter!")
label.pack()

root.mainloop()