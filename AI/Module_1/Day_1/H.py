# -------------------------------
# Extended Interactive Chatbot
# -------------------------------

print("Hello! I am AI Bot 🤖")
print("What's your name?")

# user নাম নেওয়া
name = input().strip().title()   # string manipulation
print(f"\nNice to meet you, {name}!")

# chatbot চালু রাখার জন্য loop
while True:
    print("\nHow are you feeling today?")
    print("Options: good / bad / bored / angry")
    
    mood = input("Your mood: ").lower()

    # emotion-based responses
    if mood == "good":
        print("That's awesome! 😊 Keep smiling!")
    elif mood == "bad":
        print("I'm sorry to hear that 😔 Hope things get better soon.")
    elif mood == "bored":
        print("Bored? 😴 Maybe try reading or learning something new!")
    elif mood == "angry":
        print("Take a deep breath 😤 Everything will be okay.")
    else:
        print("Hmm 🤔 I don't fully understand that feeling.")

    # extra conversation topic
    print("\nWhat would you like to talk about?")
    print("1. Motivation")
    print("2. Study tips")
    print("3. Fun fact")
    
    choice = input("Enter 1 / 2 / 3: ")

    if choice == "1":
        print("💡 Believe in yourself. Small steps lead to big success!")
    elif choice == "2":
        print("📚 Study tip: Study a little every day, not everything at once.")
    elif choice == "3":
        print("🤯 Fun fact: Python was named after a comedy show, not a snake!")
    else:
        print("😅 Invalid choice, but that's okay.")

    # repeat or end option
    again = input("\nDo you want to continue chatting? (yes/no): ").lower()

    if again == "no":
        print(f"\nIt was nice chatting with you, {name}! 👋 Goodbye!")
        break
