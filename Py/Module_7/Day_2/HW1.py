from tkinter import *
from datetime import date

root = Tk()
root.title("Age Calculator App")
root.geometry("400x400")

def calculate_age():
    name = name_entry.get()
    d = int(date_entry.get())
    m = int(month_entry.get())
    y = int(year_entry.get())

    today = date.today()
    age = today.year - y

    if (today.month, today.day) < (m, d):
        age -= 1

    result_label.config(
        text=f"Hello {name}!\nYour present age is {age} years.",
        fg="green"
    )

Label(root, text="Age Calculator", font=("Arial", 16, "bold")).pack(pady=10)


Label(root, text="Name").pack()
name_entry = Entry(root)
name_entry.pack()


Label(root, text="Date").pack()
date_entry = Entry(root)
date_entry.pack()


Label(root, text="Month").pack()
month_entry = Entry(root)
month_entry.pack()


Label(root, text="Year").pack()
year_entry = Entry(root)
year_entry.pack()


Button(root, text="Calculate Age", command=calculate_age, bg="lightblue").pack(pady=10)

result_label = Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

root.mainloop()
