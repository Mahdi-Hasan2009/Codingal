# Greet the user
print("Hello! I am AI Bot 🤖. What's your name? : ")

# Get user input
name = input()

# Respond to the user's name
print(f"Nice to meet you, {name}!")

while True:

    # Ask a question
    print("How are you feeling today? (good/bad) : ")
    mood = input().lower()

    # Use conditional statements to respond based on input
    if mood == "good":
        print("I'm glad to hear that!😊")
    elif mood == "bad":
        print("I'm sorry to hear that. Hope things get better soon.🥺")
    else:
        print("I see. Sometimes it's hard to put feelings into words.🤔")

    print("\nWhat would you want to talk about?")
    print("1.Motivation")
    print("2.Study tips")
    print("3.Fun facts")

    choice = int(input("1/2/3:   "))

    if choice == 1:
        print("Believe in yourself. Small steps lead to big success!")
    elif choice == 2:
        print("Study a little every day, not everything at once.")
    elif choice == 3 :
        print("Python was named after a comedy show, not a snake!")
    else:
        print("Invalid choice ,but thanks for staying with us!")
        
    
    again = input("\nDo you want to continue chatting? (yes/no): ").lower()
    
    if again == "no":
        # End the conversation
        print(f"\nIt was nice chatting with you, {name}! 👋 Goodbye!")
        break        

