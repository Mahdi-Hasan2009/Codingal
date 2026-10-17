'''# Greet the user 
print("Hello! I am AI Bot. What's your name? : ")

# Get user input 
name = input()

# Respond to the user's name 
print(f"Nice to meet you, {name}!")

# Ask a question
print("How are you feeling today? (good/bad) : ")
mood = input().lower()

# Use conditional statements to respond based on input
if mood == "good":
  print("I'm glad to hear that!")
elif mood == "bad":
  print("I'm sorry to hear that. Hope things get better soon.")
else:
  print("I see. Sometimes it's hard to put feelings into words.")
  
# End the conversation
print(f"It was nice chatting with you {name}. Goodbye!")'''
'''
num = int(input("Enter a number: "))

if num%2 == 0:
  print("Even")
else:
  print("Odd")
  
  
def odd_or_even(num):
  return "Even" if num ^1 == 0 else "Odd"'''


principal = float(input("Enter Your Principal: "))
rate = float(input("Enter Your Rate in percent: "))
time = float(input("Enter Your Time: "))
ratepercent = rate/100 
Compound_Amount =principal * (1+ratepercent)**time
Final_Amount = (principal*ratepercent*time)+principal
interest = principal*ratepercent*time
Compound_Interest = (principal * (1+ratepercent)**time)-principal
print("Your Interest Is: ",interest) 
print("Your Final Amount Is: ",Final_Amount)
print("Your Compound Interest Is: ",Compound_Interest)
print("Your Compound Amount Is: ",Compound_Amount)










  
  
  





