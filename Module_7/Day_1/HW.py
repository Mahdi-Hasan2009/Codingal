import tkinter as tk

root = tk.Tk()
root.title("Getting Started with Widgets")
root.geometry("400x300")

label = tk.Label(root,text="This activity aims to help you understand the basic widgets in an application")
label.pack()

def on_click():
  label.config(text="Button Clicked!")


button = tk.Button(root,text = "Click me!",command = on_click)
button.pack()


root.mainloop()
