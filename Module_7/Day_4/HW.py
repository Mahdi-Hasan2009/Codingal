from tkinter import *

window = Tk()
window.title("Age Calculator App")
window.geometry("400x400")

def calculate_interest():
    p = float(principal_entry.get())
    t = float(time_entry.get())
    r = float(rate_entry.get())

    si = (p * t * r) / 100

    
    ci = p * (1 + r/100) ** t - p

    result_label.config(
        text=f"Simple Interest = {si}\nCompound Interest = {ci}"
    )

Label(window, text="Interest Calculator", font=("Arial", 16, "bold")).pack(pady=10)

frame = Frame(window)
frame.pack(pady=10)


Label(frame, text="Principal").grid(row=0, column=0, padx=5, pady=5)
principal_entry = Entry(frame)
principal_entry.grid(row=0, column=1, padx=5, pady=5)

Label(frame, text="Time (years)").grid(row=1, column=0, padx=5, pady=5)
time_entry = Entry(frame)
time_entry.grid(row=1, column=1, padx=5, pady=5)


Label(frame, text="Rate (%)").grid(row=2, column=0, padx=5, pady=5)
rate_entry = Entry(frame)
rate_entry.grid(row=2, column=1, padx=5, pady=5)


Button(window, text="Calculate", command=calculate_interest, bg="lightgreen").pack(pady=10)

result_label = Label(window, text="", font=("Arial", 12))
result_label.pack(pady=10)

window.mainloop()
