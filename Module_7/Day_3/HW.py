from tkinter import *
from tkinter import messagebox

# Setup Tkinter Window
root = Tk()
root.title("Length Converter App")    
root.geometry("400x400")        

Label(root,text= "write a length in inches").pack()
entry1 = Entry(root)
entry1.pack()

def calculate():
  
  #entry2 = entry1
  entry2 = entry1.get()
  inches = float(entry2)
  cm = inches*2.54
  result_box.config(text= f'centimeter value {cm}')

Button(root, text="Convert", command=calculate).pack(pady=10)

result_box = Label(root,text = "")
result_box.pack()


root.mainloop()