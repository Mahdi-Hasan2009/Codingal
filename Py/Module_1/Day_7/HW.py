char = input("Enter an alphabet: ")
ascii_code = ord(char)
if len(char) == 1 and char.isalpha():
    print(f"The ASCII code of '{char}' is: {ascii_code}")
else:
    print("Please enter a single alphabet character (A-Z or a-z).")
