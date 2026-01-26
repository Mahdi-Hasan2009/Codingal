import tkinter as tk

root = tk.Tk()
root.title("Password Checker App")
root.geometry("400x400")



def check_strength():
    password = entry.get()
    length = len(password)
      

    if length <= 5:
      result_label.config(text="Weak", fg="red")
    elif 6 <= length <= 8:
      result_label.config(text="Medium", fg="yellow")
    elif 9 <= length <= 12:
      result_label.config(text="Strong", fg="light green")
    else:
      result_label.config(text="Very Strong", fg="dark green")


tk.Label(root, text="Enter Password:", font=("Arial", 12)).pack(pady=10)


entry = tk.Entry(root, show="*", font=("Arial", 12))
entry.pack(pady=10)

tk.Button(root, text="Check Strength", command=check_strength).pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 14, "bold"))
result_label.pack(pady=20)

root.mainloop()
