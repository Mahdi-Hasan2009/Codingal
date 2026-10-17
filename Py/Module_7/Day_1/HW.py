from tkinter import *

root = Tk()
root.title("Getting Started with Widgets")
root.geometry("450x300")

label = Label(root,text="This activity aims to help you understand the basic widgets in an application")
label.pack()

label2 = Label(root,text="Enter a number: ")
label2.place(x=20, y=60)
label2_entry = Entry()
label2_entry.place(x=150, y=60)

label3 = Label(root,text="Enter another number: ")
label3.place(x=20, y=90)
label3_entry = Entry()
label3_entry.place(x=150, y=90)

def display():
    sum = label2_entry+label3_entry
    message = "\nCongratulations for your new account!"
    textbox.insert(END, message)
    textbox.insert(END, sum)
  
textbox = Text(bg="#BEBEBE", fg="black",height = 50)
textbox.place(y=200)

button = Button(root,text = "Calculate",command = display)
button.place(x=100, y=120)


root.mainloop()
