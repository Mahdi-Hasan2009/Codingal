import random as random
import time 

def intro():
  
  name = input("May I ask you for your name?")
  print(name + " , we are going to play . I am     thinking of a number between 1 and 100")
  
  RandomNumber = random.randint(1,100)
  new_RandomNumber = int(RandomNumber)
  
  
  if new_RandomNumber %2 == 0:
    print("This is an even number")
    
  else:
    print("This is an odd number")
    
  print("Go ahead. Guess!")
 
  guessNum = int(input())
  while True:
    if guessNum == new_RandomNumber:
      print("You are win") 
      break
    elif guessNum < new_RandomNumber:
      print("The guess of the number that you have entered is too low")
    elif guessNum > new_RandomNumber:
      print("The guess of the number that you have entered is too high")
    guessNum = int(input("Enter again: "))
    
  play_again = input("Do you want to play again (yes/now)?").lower()
      
  if play_again == "yes":
    intro()
  else:
    print(f"Thanks {name} for playing! Goodbye")
    
    
      
   
    
intro()