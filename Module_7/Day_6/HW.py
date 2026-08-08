import tkinter as tk
import random

root = tk.Tk()
root.title("Rock, Paper, Scissors Game")

root.geometry("400x400")

def play(user):
  computer = random.choice(["Rock", "Paper", "Scissors"])

  if user == computer:
    result = "Draw"
  elif (user == "Rock" and computer == "Scissors") or \
    (user == "Paper" and computer == "Rock") or \
    (user == "Scissors" and computer == "Paper"):
    result = "You Win"
  else:
          result = "Computer Wins"

  result_label.config(
    text="You: " + user +
    "\nComputer: " + computer +
    "\nResult: " + result
)


def rock_click():
  
  play("Rock")

def paper_click():
  play("Paper")
    
    

def scissors_click():
  play("Scissors")

tk.Label(root, text="Rock Paper Scissors").pack(pady=20)

tk.Button(root, text="Rock",command=rock_click).pack(pady=10)
tk.Button(root, text="Paper", command=paper_click).pack(pady=10)
tk.Button(root, text="Scissors", command=scissors_click). pack(pady=10)



result_label = tk.Label(root,text="")
result_label.pack(pady=20)

root.mainloop()
