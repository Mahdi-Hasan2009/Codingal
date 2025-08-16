import random
choice_list = ["Rock","Paper","Scissors"]
user_choice= input("Enter Rock or Paper or Scissors ").capitalize()
computer_choice = random.choice(choice_list)




print("You chose:", user_choice)
print("Computer chose:", computer_choice)

if user_choice == computer_choice:
    print("It's a tie!")
elif user_choice == "Rock" and computer_choice == "Scissors":
    print("Rock smashes scissors! You win!")
elif user_choice == "Paper" and computer_choice == "Rock":
    print("Paper covers rock! You win!")
elif user_choice == "Scissors" and computer_choice == "Paper":
    print("Scissors cuts paper! You win!")
else:
    print("You lose!. ")
