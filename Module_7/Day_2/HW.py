from tkinter import *

# Create window
root = Tk()
root.geometry("400x300")
root.title("Getting Started with Widgets")

# Description label
Label(root, text="This application calculates the product of two numbers.").pack(pady=10)

# First number
Label(root, text="Enter first number").pack()
entry1 = Entry(root)
entry1.pack()

# Second number
Label(root, text="Enter second number").pack()
entry2 = Entry(root)
entry2.pack()

# Function to calculate product
def calculate():
    num1 = float(entry1.get())
    num2 = float(entry2.get())
    product = num1 * num2
    result_box.delete("1.0", END)
    result_box.insert(END, product)

# Button
Button(root, text="Calculate", command=calculate).pack(pady=10)

# Result label
Label(root, text="Result").pack()

# Text box to display result
result_box = Text(root, height=2, width=20)
result_box.pack()

# Run window
root.mainloop()
