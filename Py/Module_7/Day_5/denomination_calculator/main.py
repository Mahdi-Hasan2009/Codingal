"""

5 Taka

10 Taka

20 Taka

50 Taka

100 Taka

200 Taka

500 Taka

1,000 Taka

"""



from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk  # For image support

# --------------------------- Main Window Setup ---------------------------
root = Tk()
root.title("Denomination Counter")         # Set the window title
root.configure(bg='light blue')            # Set background color
root.geometry('650x400')                   # Set window size

# --------------------------- Adding Image ---------------------------
img = Image.open("note.jpg")            # Load image (ensure this file is in the same folder)
img = img.resize((400, 300))               # Resize the image
photo = ImageTk.PhotoImage(img)            # Convert to Tkinter-compatible image

img_label = Label(root, image=photo, bg='light blue')  # Image label
img_label.place(x=120, y=20)              # Place image on screen

# --------------------------- Welcome Message ---------------------------
welcome_label = Label(
    root,
    text="Hey User! Welcome to Denomination Counter Application.",
    bg='light blue',
    font=('Arial', 12)
)
welcome_label.place(relx=0.5, y=340, anchor=CENTER)   # Centered horizontally

# --------------------------- Function to Open Denomination Calculator ---------------------------
def open_top_window():
    top = Toplevel()                                 # Create a new popup window
    top.title("Denominations Calculator")
    top.configure(bg='light grey')
    top.geometry("600x350+150+50")

    # --- Widgets ---
    label = Label(top, text="Enter Amount:", font=('Arial', 12), bg='light grey')
    entry = Entry(top, font=('Arial', 12))

    lbl = Label(top, text="Breakdown of Notes", font=('Arial', 12, 'bold'), bg='light grey')
    l1 = Label(top, text="₹2000 Notes:", font=('Arial', 10), bg='light grey')
    l2 = Label(top, text="₹500 Notes:", font=('Arial', 10), bg='light grey')
    l3 = Label(top, text="₹100 Notes:", font=('Arial', 10), bg='light grey')

    t1 = Entry(top)
    t2 = Entry(top)
    t3 = Entry(top)

    # --- Calculator Logic ---
    def calculator():
        try:
            amount = int(entry.get())
            note1000 = amount // 1000
            amount %= 1000

            note500 = amount // 500
            amount %= 500

            note200 = amount // 200
            amount %= 200

            note100 = amount // 100
            amount %= 100
            
            note50 = amount // 50
            amount %= 50
            
            note20 = amount // 20
            amount %= 20
            
            note10 = amount // 10
            amount %= 10
            
            note5 = amount // 5
            amount %= 5
            
            note2 = amount // 2
            amount %= 2
            
            note1 = amount // 1
            amount %= 1

            t1.delete(0, END)   #5
            t2.delete(0, END)
            t3.delete(0, END)

            t1.insert(END, str(note1000))
            t2.insert(END, str(note500))
            t2.insert(END, str(note200))
            t3.insert(END, str(note100))
            t2.insert(END, str(note50))
            t2.insert(END, str(note20))
            t2.insert(END, str(note10))
            t2.insert(END, str(note5))
            t2.insert(END, str(note2))
            t2.insert(END, str(note1))
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    btn = Button(top, text='Calculate', command=calculator, bg='brown', fg='white', font=('Arial', 10, 'bold'))

    # --- Placement ---
    label.place(x=230, y=50)
    entry.place(x=200, y=80)
    btn.place(x=240, y=120)
    lbl.place(x=140, y=170)

    l1.place(x=180, y=200)
    l2.place(x=180, y=230)
    l3.place(x=180, y=260)

    t1.place(x=270, y=200)
    t2.place(x=270, y=230)
    t3.place(x=270, y=260)

# --------------------------- Confirmation Message Function ---------------------------
def show_message():
    response = messagebox.showinfo("Alert", "Do you want to calculate the denomination count?")
    if response == 'ok':
        open_top_window()

# --------------------------- Start Button ---------------------------
start_button = Button(
    root,
    text="Let's get started!",
    command=show_message,
    bg='brown',
    fg='white',
    font=('Arial', 11, 'bold')
)
start_button.place(x=260, y=360)

# --------------------------- Mainloop ---------------------------
root.mainloop()
