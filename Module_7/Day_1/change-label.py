import tkinter as tk

root = tk.Tk()
root.title("My first Tkinter window")
root.geometry("800x500")

def on_click():
  label.config(text="Button Clicked!")

label = tk.Label(root,text="Hi, Tkinter!")
label.pack()

button = tk.Button(root,text = "Click me!",command = on_click)
button.pack()


root.mainloop()